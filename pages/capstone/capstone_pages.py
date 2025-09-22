from locators.map_locators import MapLocators
from locators.project_locators import CapstonePageLocators

from ..base_page import BasePage


class CapstonePages(BasePage):
    """Класс для работы со страницами Capstone проектов (Peylaa)."""

    def __init__(self, page, url: str = None):
        """Инициализация CapstonePages.

        Args:
            page: Playwright page объект
            url: URL страницы (если не указан, будет использован Capstone map URL)
        """
        if url is None:
            from conftest import _get_urls_by_environment

            urls = _get_urls_by_environment()
            url = urls["capstone_map"]

        super().__init__(page, url, CapstonePageLocators)
        self.map_locators = MapLocators()

    def get_project_url(self, project_name: str, page_type: str = "area") -> str:
        """Получить URL для Capstone проекта.

        Args:
            project_name: Название проекта (peylaa)
            page_type: Тип страницы (area, map)

        Returns:
            str: URL для проекта
        """
        from conftest import _get_urls_by_environment

        urls = _get_urls_by_environment()
        project_name_lower = project_name.lower()

        if project_name_lower not in ["peylaa"]:
            raise ValueError(f"Неизвестный Capstone проект: {project_name}")

        base_url = urls["capstone_map"].replace("/map", "")

        if page_type == "area":
            return f"{base_url}/project/{project_name_lower}/area"
        elif page_type == "map":
            return urls["capstone_map"]
        else:
            raise ValueError(f"Неизвестный тип страницы для Capstone: {page_type}")

    def click_project_on_map(self, project_name: str):
        """Кликнуть на проект на карте Capstone."""
        if project_name.lower() == "peylaa":
            import os

            environment = os.getenv("TEST_ENVIRONMENT", "dev")
            if environment == "dev":
                self.click('img[src*="map_pin_peylaa.png"]')
            else:
                self.click('div[aria-label*="Peylaa"]')
        else:
            raise ValueError(f"Неизвестный Capstone проект: {project_name}")

        self.wait_for_page_load()
