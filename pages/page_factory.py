"""Фабрика для создания page objects."""

from config.environments import environment_manager
from core.base_page import BasePage
from locators import locators
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
            env_config = environment_manager.get_environment()
            return BasePage(page, env_config.base_url, QubeLocators)
        else:
            return page_objects[developer_type](page)
