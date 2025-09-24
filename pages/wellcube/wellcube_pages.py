from locators.map_locators import MapLocators
from locators.project_locators import WellcubePageLocators

from ..base_page import BasePage


class WellcubePages(BasePage):
    """Класс для работы со страницами Wellcube проектов (Tranquil)."""

    def __init__(self, page, url: str = None):
        """Инициализация WellcubePages.

        Args:
            page: Playwright page объект
            url: URL страницы (если не указан, будет использован Wellcube map URL)
        """
        if url is None:
            from conftest import _get_urls_by_environment

            urls = _get_urls_by_environment()
            url = urls["wellcube_map"]

        super().__init__(page, url, WellcubePageLocators)
        self.map_locators = MapLocators()

    def get_project_url(self, project_name: str, page_type: str = "catalog2d") -> str:
        """Получить URL для Wellcube проекта.

        Args:
            project_name: Название проекта (tranquil)
            page_type: Тип страницы (catalog2d, area, map)

        Returns:
            str: URL для проекта
        """
        from conftest import _get_urls_by_environment

        urls = _get_urls_by_environment()
        project_name_lower = project_name.lower()

        if project_name_lower not in ["tranquil"]:
            raise ValueError(f"Неизвестный Wellcube проект: {project_name}")

        base_url = urls["wellcube_map"].replace("/map", "")

        if page_type == "catalog2d":
            return f"{base_url}/project/{project_name_lower}/catalog_2d"
        elif page_type == "area":
            return f"{base_url}/project/{project_name_lower}/area"
        elif page_type == "map":
            return urls["wellcube_map"]
        else:
            raise ValueError(f"Неизвестный тип страницы: {page_type}")

    def click_on_fraction_ownership_offer_button(self):
        """Кликнуть на кнопку "Скачать ownership offer"""
        self.expect_visible(
            self.project_locators.Tranquil.FRACTION_OWNERSHIP_OFFER_BUTTON
        )
        self.click(self.project_locators.Tranquil.FRACTION_OWNERSHIP_OFFER_BUTTON)
