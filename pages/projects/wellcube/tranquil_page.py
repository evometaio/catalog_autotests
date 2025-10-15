"""Страница проекта Tranquil (Wellcube)."""

from playwright.sync_api import Page

from pages.base_page import BasePage
from pages.components.map_component import MapComponent
from pages.components.amenities_component import AmenitiesComponent
from pages.components.area_tour_360_component import AreaTour360Component
from locators.wellcube.tranquil_locators import TranquilLocators


class TranquilPage(BasePage):
    """
    Страница проекта Tranquil.
    
    Наследует от BasePage и добавляет специфичную функциональность Tranquil.
    """

    def __init__(self, page: Page, url: str = None):
        """
        Инициализация Tranquil страницы.
        
        Args:
            page: Playwright Page объект
            url: URL страницы
        """
        if url is None:
            from conftest import _get_urls_by_environment
            urls = _get_urls_by_environment()
            url = urls["wellcube_map"]
        
        super().__init__(page, url, TranquilLocators)
        
        # Переопределяем компоненты с правильными локаторами
        self.map = MapComponent(page, self.project_locators)
        self.amenities = AmenitiesComponent(page, self.project_locators)
        self.area_tour_360 = AreaTour360Component(page, self.project_locators)
        
        # Устанавливаем название проекта
        self.project_name = "tranquil"

    def click_fraction_ownership_offer_button(self):
        """Кликнуть на кнопку Fraction Ownership Offer (специфично для Tranquil)."""
        self.browser.click(self.project_locators.FRACTION_OWNERSHIP_OFFER_BUTTON)
    
    def click_download_pdf_button(self):
        """Кликнуть на кнопку Download PDF."""
        self.browser.click(self.project_locators.DOWNLOAD_PDF_BUTTON)

