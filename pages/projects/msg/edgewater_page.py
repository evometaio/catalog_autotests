"""Страница проекта Edgewater (MSG)."""

from playwright.sync_api import Page

from locators.msg.edgewater_locators import EdgewaterLocators
from pages.base_page import BasePage
from pages.components.amenities_component import AmenitiesComponent
from pages.components.area_tour_360_component import AreaTour360Component
from pages.components.map_component import MapComponent


class EdgewaterPage(BasePage):
    """
    Страница проекта Edgewater.

    Наследует от BasePage и добавляет специфичную функциональность Edgewater.
    """

    def __init__(self, page: Page, url: str = None):
        """
        Инициализация Edgewater страницы.

        Args:
            page: Playwright Page объект
            url: URL страницы
        """
        if url is None:
            from conftest import _get_urls_by_environment

            urls = _get_urls_by_environment()
            url = urls["msg_edgewater"]

        super().__init__(page, url, EdgewaterLocators)

        # Переопределяем компоненты с правильными локаторами
        self.map = MapComponent(page, self.project_locators)
        self.amenities = AmenitiesComponent(page, self.project_locators)
        self.area_tour_360 = AreaTour360Component(page, self.project_locators)

        # Устанавливаем название проекта
        self.project_name = "edgewater"
