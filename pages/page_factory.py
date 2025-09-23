"""Фабрика для создания page objects."""

from conftest import _get_urls_by_environment
from locators.project_locators import QubeLocators
from pages.base_page import BasePage
from pages.capstone.capstone_pages import CapstonePages
from pages.wellcube.wellcube_pages import WellcubePages


class PageFactory:
    """Фабрика для создания page objects по типу застройщика."""

    @staticmethod
    def get_page_object(page, developer_type: str):
        """Получить page object для указанного застройщика.

        Args:
            page: Playwright Page объект
            developer_type: Тип застройщика ('qube', 'wellcube', 'capstone')

        Returns:
            Соответствующий page object
        """
        page_objects = {
            "qube": BasePage,
            "wellcube": WellcubePages,
            "capstone": CapstonePages,
        }

        if developer_type not in page_objects:
            raise ValueError(f"Неизвестный тип застройщика: {developer_type}")

        if developer_type == "qube":

            urls = _get_urls_by_environment()
            return BasePage(page, urls["map"], QubeLocators)
        else:
            return page_objects[developer_type](page)
