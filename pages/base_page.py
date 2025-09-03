import os
from playwright.sync_api import Locator, Page, expect

from locators.map_locators import MapLocators
from locators.project_locators import QubePageLocators


class BasePage:
    """Базовый класс для всех страниц."""

    # Константы для таймаутов
    DEFAULT_TIMEOUT = 20000
    LONG_TIMEOUT = 30000
    SHORT_TIMEOUT = 5000
    MAP_LOAD_TIMEOUT = 30000

    def __init__(self, page: Page, base_url: str = None):
        self.locators = MapLocators()
        self.page = page
        self.base_url = base_url
        
        # URL-ы для навигации (если base_url содержит /map)
        if base_url and "/map" in base_url:
            self.project_url_template = base_url.replace("/map", "/project/{project}/area")
            self.map_url = base_url

    def open(self, path: str = "", route_type: str = None):
        """Открыть страницу.

        Args:
            path: Дополнительный путь к базовому URL
            route_type: Тип роута для проверки - "client", "agent" или "map"
        """
        url = (
            f"{self.base_url.rstrip('/')}/{path.lstrip('/')}" if path else self.base_url
        )
        self.page.goto(url)
        self.wait_for_page_load()
        
        # Принудительно сбрасываем масштаб страницы
        self.page.evaluate("document.body.style.zoom = '1'")
        self.page.evaluate("document.documentElement.style.zoom = '1'")

        current_url = self.get_current_url()
        assert (
            url in current_url
        ), f"Не удалось открыть страницу. Ожидалось: {url}, Получено: {current_url}"
        
        # Проверяем тип роута, если указан
        if route_type:
            if route_type == "client":
                assert "client" in current_url, f"Не открылась клиентская страница. URL: {current_url}"
            elif route_type == "agent":
                assert "agent" in current_url, f"Не открылась агентская страница. URL: {current_url}"
            elif route_type == "map":
                assert "map" in current_url, f"Не открылась страница карты. URL: {current_url}"


    def wait_for_element(self, selector: str, timeout: int = None) -> Locator:
        """Ожидать появления элемента."""
        if timeout is None:
            timeout = self.DEFAULT_TIMEOUT
        element = self.page.locator(selector)
        element.wait_for(state="visible", timeout=timeout)
        return element

    def get_current_url(self) -> str:
        """Получить текущий URL."""
        return self.page.url

    def wait_for_map_and_projects_loaded(self):
        """Ожидать полной загрузки карты и проектов."""
        try:
            # Сначала ждем загрузки контейнера карты
            self.wait_for_element(self.locators.MAP_CONTAINER, timeout=self.MAP_LOAD_TIMEOUT)

            # Затем ждем появления хотя бы одного проекта
            # Используем локатор из MapLocators вместо хардкода
            self.page.wait_for_selector(
                self.locators.ALL_PROJECTS_SELECTOR,
                state="visible",
                timeout=self.MAP_LOAD_TIMEOUT,
            )

            # Дополнительная пауза для стабилизации карты
            self.page.wait_for_timeout(2000)

        except Exception as e:
            print(f"Ошибка при ожидании загрузки карты: {e}")

    def click(self, selector: str, timeout: int = None):
        """Кликнуть по элементу."""
        element = self.wait_for_element(selector, timeout)
        expect(element).to_be_enabled()
        expect(element).to_be_visible()
        element.click()

    def fill(self, selector: str, text: str, timeout: int = None):
        """Заполнить поле."""
        element = self.wait_for_element(selector, timeout)
        element.fill(text)

    def get_text(self, selector: str, timeout: int = None) -> str:
        """Получить текст элемента."""
        element = self.wait_for_element(selector, timeout)
        return element.text_content()

    def is_visible(self, selector: str, timeout: int = None) -> bool:
        """Проверить видимость элемента."""
        try:
            self.wait_for_element(selector, timeout)
            return True
        except:
            return False

    def expect_visible(self, selector: str, timeout: int = None):
        """Ожидать видимости элемента."""
        element = self.wait_for_element(selector, timeout)
        expect(element).to_be_visible()

    def wait_for_page_load(self):
        """Ожидать загрузки страницы."""
        self.page.wait_for_load_state("networkidle")

    def assert_url_equals(self, expected_url: str, timeout: int = None):
        """Проверить, что URL точно равен ожидаемому.

        Args:
            expected_url: Ожидаемый URL
            timeout: Таймаут ожидания изменения URL
        """
        if timeout is None:
            timeout = self.SHORT_TIMEOUT
        current_url = self.get_current_url()
        assert (
            current_url == expected_url
        ), f"URL не совпадает. Ожидалось: {expected_url}, Получено: {current_url}"

    # Методы для работы с картой (из MapPage)



    def check_map_loaded(self):
        """Проверить загрузку карты."""
        self.expect_visible(self.locators.MAP_CONTAINER)


    def click_project(self, project_name: str):
        """Кликнуть по проекту на карте по названию."""
        # Получаем правильный локатор для проекта
        selector = self._get_project_selector(project_name)
        
        # Ждем появления проекта
        self.page.wait_for_selector(selector, state="visible", timeout=10000)
        self.click(selector)
    
    def _get_project_selector(self, project_name: str) -> str:
        """Получить селектор для проекта по названию."""
        project_name_lower = project_name.lower()
        
        # Маппинг проектов на их селекторы
        project_selectors = {
            "elire": 'div[aria-label*="Elire"], div[aria-label*="ELIRE"]',
            "arisha": 'div[aria-label*="ARISHA TERACCES"], div[aria-label*="Arisha"], div[aria-label*="ARISHA"]',
            "cubix": 'div[aria-label*="CUBIX RESIDENCE"], div[aria-label*="Cubix"], div[aria-label*="CUBIX"]',
            "peylaa": 'li:has-text("peylaa"), span:has-text("Peylaa"), div[aria-label*="Peylaa"], div[aria-label*="PEYLAA"]',
            "tranquil": 'li:has-text("tranquil"), span:has-text("Tranquil"), div[aria-label*="Tranquil"], div[aria-label*="TRANQUIL"]'
        }
        
        if project_name_lower in project_selectors:
            return project_selectors[project_name_lower]
        else:
            # Fallback на старый способ
            return f'div[aria-label*="{project_name}"], div[aria-label*="{project_name.upper()}"]'

    def check_project_info_visible(self, project_name: str):
        """Проверить видимость информации о проекте."""
        self.expect_visible(self.locators.PROJECT_INFO_WINDOW)

    def open_project_page(self, project_name: str):
        """Открыть страницу проекта."""
        # Находим проект по имени
        project = None
        for p in QubePageLocators.ALL_PROJECTS:
            if p.PROJECT_NAME == project_name.lower():
                project = p
                break

        if not project:
            available_projects = [p.PROJECT_NAME for p in QubePageLocators.ALL_PROJECTS]
            raise ValueError(
                f"Неизвестный проект Qube: {project_name}. Доступные: {available_projects}"
            )

        project_url = self.project_url_template.format(project=project.PROJECT_NAME)
        self.page.goto(project_url)
        self.wait_for_page_load()

    def check_project_page_loaded(self, project_name: str):
        """Проверить загрузку страницы проекта."""
        # Находим проект по имени
        project = None
        for p in QubePageLocators.ALL_PROJECTS:
            if p.PROJECT_NAME == project_name.lower():
                project = p
                break

        if not project:
            raise ValueError(f"Неизвестный проект Qube: {project_name}")

        # Проверяем, что мы на странице проекта (URL содержит /project/ и название проекта)
        self.wait_for_page_load()
        current_url = self.page.url
        self.wait_for_page_load()
        assert (
            f"/project/{project.PROJECT_NAME}" in current_url
        ), f"Не на странице проекта {project.PROJECT_DISPLAY_NAME}. Текущий URL: {current_url}"

    def return_to_map_from_project(self):
        """Вернуться на карту со страницы проекта."""
        self.page.goto(self.map_url)
        self.wait_for_page_load()

    def verify_returned_to_map(self):
        """Проверить, что вернулись на карту."""
        current_url = self.page.url
        assert (
            self.map_url in current_url
        ), f"Не вернулись на карту. Текущий URL: {current_url}"

    def toggle_fullscreen(self):
        """Переключить полноэкранный режим."""
        try:
            # Сначала пробуем основной локатор
            if self.is_visible(self.locators.FULLSCREEN_BUTTON, timeout=5000):
                self.click(self.locators.FULLSCREEN_BUTTON)
            else:
                # Пробуем альтернативные локаторы
                self.click(self.locators.FULLSCREEN_ALT)
        except Exception:
            # Если не удалось, просто логируем
            print("Кнопка полноэкранного режима не найдена или недоступна")
