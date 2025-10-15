"""Базовая страница - минимальная ответственность."""

from playwright.sync_api import Page

from locators.map_locators import MapLocators
from locators.base_locators import BaseLocators
from pages.core.browser_actions import BrowserActions
from pages.core.assertions import Assertions
from pages.components.map_component import MapComponent
from pages.components.amenities_component import AmenitiesComponent


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
            self.project_url_template = base_url.replace("/map", "/project/{project}/area")
            self.map_url = base_url

        # Композиция компонентов
        self.browser = BrowserActions(page)
        self.assertions = Assertions(page)
        self.map = MapComponent(page, self.project_locators)
        self.amenities = AmenitiesComponent(page, self.project_locators)

    def open(self, path: str = "", route_type: str = None):
        """
        Открыть страницу.
        
        Args:
            path: Дополнительный путь к базовому URL
            route_type: Тип роута для проверки - "client", "agent" или "map"
        """
        url = f"{self.base_url.rstrip('/')}/{path.lstrip('/')}" if path else self.base_url
        self.page.goto(url)
        self.wait_for_page_load()

        # Принудительно сбрасываем масштаб страницы
        self.page.evaluate("document.body.style.zoom = '1'")
        self.page.evaluate("document.documentElement.style.zoom = '1'")

        current_url = self.get_current_url()
        assert url in current_url, \
            f"Не удалось открыть страницу. Ожидалось: {url}, Получено: {current_url}"

        # Проверяем тип роута, если указан
        if route_type:
            if route_type == "client":
                assert "client" in current_url, f"Не открылась клиентская страница. URL: {current_url}"
            elif route_type == "agent":
                assert "agent" in current_url, f"Не открылась агентская страница. URL: {current_url}"
            elif route_type == "map":
                assert "map" in current_url, f"Не открылась страница карты. URL: {current_url}"

    def get_current_url(self) -> str:
        """Получить текущий URL."""
        return self.page.url

    def wait_for_page_load(self):
        """Ожидать загрузки страницы."""
        self.page.wait_for_load_state("domcontentloaded")

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
                    self.page.wait_for_selector(".ant-modal-content", state="hidden", timeout=15000)
                except:
                    error_elements = self.page.locator(".ant-message-error, .ant-form-item-explain-error")
                    if error_elements.count() > 0:
                        raise AssertionError(f"Ошибка авторизации: {error_elements.text_content()}")
                    else:
                        self.browser.click(".ant-modal-close")
                        self.page.wait_for_selector(".ant-modal-content", state="hidden", timeout=5000)
            else:
                raise AssertionError("Не заданы переменные окружения USERNAME_ELIRE и PASSWORD_ELIRE")
