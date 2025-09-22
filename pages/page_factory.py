"""Фабрика для создания page objects."""

from pages.capstone.capstone_pages import CapstonePages
from pages.qube.qube_pages import QubePages
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
            "qube": QubePages,
            "wellcube": WellcubePages,
            "capstone": CapstonePages,
        }

        if developer_type not in page_objects:
            raise ValueError(f"Неизвестный тип застройщика: {developer_type}")

        return page_objects[developer_type](page)
