"""Страница проекта Peylaa (Capstone)."""

from playwright.sync_api import Page

from pages.base_page import BasePage
from pages.components.map_component import MapComponent
from pages.components.amenities_component import AmenitiesComponent
from pages.components.area_tour_360_component import AreaTour360Component
from locators.capstone.peylaa_locators import PeylaaLocators


class PeylaaPage(BasePage):
    """
    Страница проекта Peylaa.
    
    Наследует от BasePage и добавляет специфичную функциональность Peylaa.
    """

    def __init__(self, page: Page, url: str = None):
        """
        Инициализация Peylaa страницы.
        
        Args:
            page: Playwright Page объект
            url: URL страницы
        """
        if url is None:
            from conftest import _get_urls_by_environment
            urls = _get_urls_by_environment()
            url = urls["capstone_map"]
        
        super().__init__(page, url, PeylaaLocators)
        
        # Переопределяем компоненты с правильными локаторами
        self.map = MapComponent(page, self.project_locators)
        self.amenities = AmenitiesComponent(page, self.project_locators)
        self.area_tour_360 = AreaTour360Component(page, self.project_locators)
        
        # Устанавливаем название проекта
        self.project_name = "peylaa"

    # Специфичные методы для Peylaa могут быть добавлены здесь

