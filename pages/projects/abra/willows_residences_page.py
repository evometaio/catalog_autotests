"""Страница проекта Willows Residences (Abra)."""

from playwright.sync_api import Page

from locators.abra.willows_residences_locators import WillowsResidencesLocators
from pages.base_page import BasePage
from pages.components.amenities_component import AmenitiesComponent
from pages.components.area_tour_360_component import AreaTour360Component
from pages.components.map_component import MapComponent


class WillowsResidencesPage(BasePage):
    """
    Страница проекта Willows Residences.

    Наследует от BasePage и добавляет специфичную функциональность Willows Residences.
    """

    def __init__(self, page: Page, url: str = None):
        """
        Инициализация Willows Residences страницы.

        Args:
            page: Playwright Page объект
            url: URL страницы
        """
        if url is None:
            from conftest import _get_urls_by_environment

            urls = _get_urls_by_environment()
            url = urls["abra_willows_residences"]

        super().__init__(page, url, WillowsResidencesLocators)

        # Переопределяем компоненты с правильными локаторами
        self.map = MapComponent(page, self.project_locators)
        self.amenities = AmenitiesComponent(page, self.project_locators)
        self.area_tour_360 = AreaTour360Component(page, self.project_locators)

        # Устанавливаем название проекта
        self.project_name = "willows_residences"
