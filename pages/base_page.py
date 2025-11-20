"""Базовая страница - минимальная ответственность."""

from playwright.sync_api import Page

from locators.base_locators import BaseLocators
from locators.map_locators import MapLocators
from pages.components.amenities_component import AmenitiesComponent
from pages.components.map_component import MapComponent
from pages.core.assertions import Assertions
from pages.core.browser_actions import BrowserActions


class BasePage:
    """
    Базовый класс для всех страниц.

    Ответственность:
    - Инициализация Page объекта
    - Композиция базовых компонентов
    - Базовая навигация
    """

    # Константы таймаутов
    DEFAULT_TIMEOUT = 10000
    LONG_TIMEOUT = 15000
    SHORT_TIMEOUT = 5000
    MAP_LOAD_TIMEOUT = 20000

    def __init__(self, page: Page, base_url: str = None, locators_class: type = None):
        """
        Инициализация базовой страницы.

        Args:
            page: Playwright Page объект
            base_url: Базовый URL приложения
            locators_class: Класс локаторов проекта
        """
        self.page = page
        self.base_url = base_url

        # Локаторы
        self.map_locators = MapLocators()
        if locators_class:
            self.project_locators = locators_class()
        else:
            self.project_locators = BaseLocators()

        # URL-ы для навигации (если base_url содержит /map)
        if base_url and "/map" in base_url:
            self.project_url_template = base_url.replace(
                "/map", "/project/{project}/area"
            )
            self.map_url = base_url
            self.has_map = True
        else:
            self.has_map = False

        # Композиция компонентов
        self.browser = BrowserActions(page)
        self.assertions = Assertions(page)

        # MapComponent создаем только если есть /map роут
        if self.has_map:
            self.map = MapComponent(page, self.project_locators)

        self.amenities = AmenitiesComponent(page, self.project_locators)

    def open(self, path: str = "", route_type: str = None):
        """
        Открыть страницу.

        Args:
            path: Дополнительный путь к базовому URL
            route_type: Тип роута - "client", "agent" или "map".
                       Если указан, изменяет URL соответственно.
                       Игнорируется для проектов без /map роута.
        """
        # Определяем URL
        url = self.base_url

        # Если указан route_type и есть /map роут, изменяем URL
        if route_type and route_type != "map" and self.has_map:
            # Для agent и client меняем /map на /agent/map или /client/map
            if "/map" in url and route_type in ["agent", "client"]:
                url = url.replace("/map", f"/{route_type}/map")

        # Добавляем дополнительный путь если есть
        if path:
            url = f"{url.rstrip('/')}/{path.lstrip('/')}"

        self.page.goto(url)
        self.wait_for_page_load()

        # Принудительно сбрасываем масштаб страницы
        self.page.evaluate("document.body.style.zoom = '1'")
        self.page.evaluate("document.documentElement.style.zoom = '1'")

        current_url = self.get_current_url()

        # Проверяем тип роута, если указан и есть /map роут
        if route_type and self.has_map:
            self.assertions.assert_that(
                route_type in current_url,
                f"Не открылась страница {route_type}. URL: {current_url}",
            )

    def get_current_url(self) -> str:
        """Получить текущий URL."""
        return self.page.url

    def wait_for_page_load(self):
        """Ожидать загрузки страницы."""
        self.page.wait_for_load_state("domcontentloaded")

    def return_to_map(self):
        """Вернуться на карту через кнопку навигации."""
        # Используем .last т.к. на некоторых страницах (Cubix) может быть несколько элементов с этим локатором
        self.page.locator(self.project_locators.NAV_MAP_BUTTON).last.click()
        self.page.wait_for_timeout(2000)

    def get_project_url(self, project_name: str, page_type: str = "catalog_2d"):
        """
        Получить URL для конкретного проекта и типа страницы.

        Args:
            project_name: Название проекта
            page_type: Тип страницы (catalog_2d, area, map)

        Returns:
            str: URL для проекта
        """
        from conftest import _get_urls_by_environment

        urls = _get_urls_by_environment()
        project_name_lower = project_name.lower()

        # Определяем к какой группе относится проект
        qube_projects = ["arisha", "cubix", "elire"]
        capstone_projects = ["peylaa"]
        wellcube_projects = ["tranquil"]

        # Определяем базовый URL
        if project_name_lower in qube_projects:
            base_url = urls["map"].replace("/map", "")
            map_url = urls["map"]
        elif project_name_lower in capstone_projects:
            base_url = urls["capstone_map"].replace("/map", "")
            map_url = urls["capstone_map"]
        elif project_name_lower in wellcube_projects:
            base_url = urls["wellcube_map"].replace("/map", "")
            map_url = urls["wellcube_map"]
        else:
            raise ValueError(f"Неизвестный проект: {project_name}")

        # Формируем URL
        if page_type == "catalog_2d":
            return f"{base_url}/project/{project_name_lower}/catalog_2d"
        elif page_type == "area":
            return f"{base_url}/project/{project_name_lower}/area"
        elif page_type == "map":
            return map_url

    def handle_auth_modal_if_present(self):
        """Обработать модальное окно авторизации для Elire."""
        import os

        if self.browser.is_visible(".ant-modal-content", timeout=5000):
            username = os.getenv("USERNAME_ELIRE")
            password = os.getenv("PASSWORD_ELIRE")

            if username and password:
                self.browser.fill("#username", username)
                self.browser.fill("#password", password)
                self.browser.click("button[data-test-id='modal-form-primary-button']")

                try:
                    self.page.wait_for_selector(
                        ".ant-modal-content", state="hidden", timeout=15000
                    )
                except:
                    error_elements = self.page.locator(
                        ".ant-message-error, .ant-form-item-explain-error"
                    )
                    if error_elements.count() > 0:
                        raise AssertionError(
                            f"Ошибка авторизации: {error_elements.text_content()}"
                        )
                    else:
                        self.browser.click(".ant-modal-close")
                        self.page.wait_for_selector(
                            ".ant-modal-content", state="hidden", timeout=5000
                        )
            else:
                raise AssertionError(
                    "Не заданы переменные окружения USERNAME_ELIRE и PASSWORD_ELIRE"
                )
