"""Страница проекта MARK (LSR)."""

from playwright.sync_api import Page

from locators.lsr.mark_locators import MarkLocators
from pages.base_page import BasePage
from pages.components.amenities_component import AmenitiesComponent
from pages.components.apartment_widget_component import ApartmentWidgetComponent
from pages.components.area_tour_360_component import AreaTour360Component
from pages.components.navigation_component import NavigationComponent


class MarkPage(BasePage):
    """
    Страница проекта MARK.

    Наследует от BasePage и добавляет специфичную функциональность MARK.
    Особенность: нет /map роута, только /area, нет agent и client routes.
    """

    def __init__(self, page: Page, url: str = None):
        """
        Инициализация MARK страницы.

        Args:
            page: Playwright Page объект
            url: URL страницы
        """
        if url is None:
            from conftest import _get_urls_by_environment

            urls = _get_urls_by_environment()
            url = urls["lsr_mark"]

        super().__init__(page, url, MarkLocators)

        # Переопределяем компоненты с правильными локаторами
        # MapComponent не нужен, так как нет карты
        self.amenities = AmenitiesComponent(page, self.project_locators)
        self.area_tour_360 = AreaTour360Component(page, self.project_locators)
        self.navigation = NavigationComponent(page, self.project_locators)
        self.apartment_widget = ApartmentWidgetComponent(page, MarkLocators, "mark")

        # Устанавливаем название проекта
        self.project_name = "mark"

    def click_all_units_button(self):
        """Кликнуть на кнопку Все квартиры (переход в каталог)."""
        self.browser.click(self.project_locators.NAV_DESKTOP_CATALOG2D_STANDALONE)
        self.page.wait_for_url("**/catalog_2d", timeout=10000)

    def click_contact_button(self):
        """Кликнуть на кнопку Оставить заявку."""
        self.browser.click(self.project_locators.CONTACT_BUTTON)

    def click_360_panorama_menu_item(self, menu_item: str = "yard"):
        """
        Кликнуть на пункт меню панорам.

        Args:
            menu_item: Тип панорамы - "rotation", "yard", "lobby-k1", "lobby-k2", "lobby-k3"
        """
        menu_selectors = {
            "rotation": self.project_locators.AREA_TOUR_360_MENU_ROTATION,
            "yard": self.project_locators.AREA_TOUR_360_MENU_TOUR_YARD,
            "lobby-k1": self.project_locators.AREA_TOUR_360_MENU_TOUR_LOBBY_K1,
            "lobby-k2": self.project_locators.AREA_TOUR_360_MENU_TOUR_LOBBY_K2,
            "lobby-k3": self.project_locators.AREA_TOUR_360_MENU_TOUR_LOBBY_K3,
        }

        selector = menu_selectors.get(menu_item)
        if not selector:
            raise ValueError(f"Неизвестный пункт меню: {menu_item}")

        self.browser.click(selector)

    def open(self, path: str = "", route_type: str = None):
        """
        Открыть страницу MARK.

        Args:
            path: Дополнительный путь к базовому URL
            route_type: Игнорируется для MARK (нет agent/client routes)
        """
        # Для MARK игнорируем route_type, так как нет agent/client routes
        url = self.base_url

        # Добавляем дополнительный путь если есть
        if path:
            url = f"{url.rstrip('/')}/{path.lstrip('/')}"

        self.page.goto(url)
        self.wait_for_page_load()

        # Принудительно сбрасываем масштаб страницы
        self.page.evaluate("document.body.style.zoom = '1'")
        self.page.evaluate("document.documentElement.style.zoom = '1'")
