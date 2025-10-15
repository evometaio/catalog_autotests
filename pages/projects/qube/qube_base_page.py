"""Базовая страница для всех Qube проектов."""

from playwright.sync_api import Page

from pages.base_page import BasePage
from pages.components.map_component import MapComponent
from pages.components.amenities_component import AmenitiesComponent
from pages.components.navigation_component import NavigationComponent
from pages.components.apartment_widget_component import ApartmentWidgetComponent
from pages.components.apartment_info_component import ApartmentInfoComponent
from pages.components.area_tour_360_component import AreaTour360Component
from locators.base_locators import BaseLocators


class QubeBasePage(BasePage):
    """
    Базовая страница для всех Qube проектов (Arisha, Elire, Cubix).
    
    Содержит общую инициализацию и методы для всех Qube проектов.
    Каждый конкретный проект наследуется от этого класса и добавляет свою специфику.
    """

    def __init__(self, page: Page, project_name: str, url: str = None, locators_class: type = None):
        """
        Инициализация Qube страницы.
        
        Args:
            page: Playwright Page объект
            project_name: Название проекта (arisha, elire, cubix)
            url: URL страницы (если None, берется из окружения)
            locators_class: Класс локаторов проекта (если None, используется QubeLocators)
        """
        # Получаем URL из окружения если не передан
        if url is None:
            from conftest import _get_urls_by_environment
            urls = _get_urls_by_environment()
            url = urls["map"]
        
        # Используем переданный класс локаторов или BaseLocators по умолчанию
        if locators_class is None:
            locators_class = BaseLocators
        
        # Инициализируем базовый класс
        super().__init__(page, url, locators_class)
        
        # Сохраняем название проекта
        self.project_name = project_name
        
        # Композиция компонентов (общие для всех Qube проектов)
        self.map = MapComponent(page, self.project_locators)
        self.amenities = AmenitiesComponent(page, self.project_locators)
        self.navigation = NavigationComponent(page, self.project_locators)
        self.apartment_widget = ApartmentWidgetComponent(page, locators_class, project_name)
        self.apartment_info = ApartmentInfoComponent(page, locators_class, project_name)
        self.area_tour_360 = AreaTour360Component(page, self.project_locators)

    # ==================== ОБЩИЕ МЕТОДЫ ДЛЯ ВСЕХ QUBE ПРОЕКТОВ ====================
    
    def click_all_units_button(self):
        """Кликнуть на кнопку All Units (общее для всех Qube проектов)."""
        self.browser.click(self.project_locators.ALL_UNITS_BUTTON)
        self.page.wait_for_url("**/catalog_2d", timeout=10000)

    def click_sales_offer_button(self):
        """Кликнуть на кнопку Sales Offer (для агентских страниц, общее для всех Qube)."""
        self.browser.click(self.project_locators.SALES_OFFER_BUTTON)

