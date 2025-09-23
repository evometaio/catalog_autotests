from locators.map_locators import MapLocators
from locators.project_locators import QubePageLocators

from ..base_page import BasePage


class QubePages(BasePage):
    """Базовый класс для всех страниц Qube проектов (Arisha, Cubix, Elire)."""

    def __init__(self, page, url: str = None):
        """Инициализация QubeBasePage.

        Args:
            page: Playwright page объект
            url: URL страницы (если не указан, будет использован Qube map URL)
        """
        if url is None:
            from conftest import _get_urls_by_environment

            urls = _get_urls_by_environment()
            url = urls["map"]

        super().__init__(page, url, QubePageLocators)
        self.map_locators = MapLocators()

    def get_project_url(self, project_name: str, page_type: str = "catalog2d") -> str:
        """Получить URL для Qube проекта.

        Args:
            project_name: Название проекта (arisha, cubix, elire)
            page_type: Тип страницы (catalog2d, area, map)

        Returns:
            str: URL для проекта
        """
        from conftest import _get_urls_by_environment

        urls = _get_urls_by_environment()
        project_name_lower = project_name.lower()

        if project_name_lower not in ["arisha", "cubix", "elire"]:
            raise ValueError(f"Неизвестный Qube проект: {project_name}")

        base_url = urls["map"].replace("/map", "")

        if page_type == "catalog2d":
            return f"{base_url}/project/{project_name_lower}/catalog_2d"
        elif page_type == "area":
            return f"{base_url}/project/{project_name_lower}/area"
        elif page_type == "map":
            return urls["map"]
        else:
            raise ValueError(f"Неизвестный тип страницы: {page_type}")

    def click_project_on_map(self, project_name: str):
        """Кликнуть на проект на карте Qube."""
        project_selector = self._get_project_selector(project_name)
        self.click(project_selector)
        self.wait_for_page_load()

    def _get_project_selector(self, project_name: str) -> str:
        """Получить селектор для проекта Qube."""
        project_name_lower = project_name.lower()

        project_selectors = {
            "elire": 'div[aria-label="Elire"]',
            "arisha": 'div[aria-label*="ARISHA TERACCES"], div[aria-label*="Arisha"], div[aria-label*="ARISHA"]',
            "cubix": 'div[aria-label*="CUBIX RESIDENCE"], div[aria-label*="Cubix"], div[aria-label*="CUBIX"]',
        }

        if project_name_lower in project_selectors:
            return project_selectors[project_name_lower]
        else:
            raise ValueError(f"Неизвестный Qube проект: {project_name}")

    def click_on_residences_button(self):
        """Кликнуть на кнопку Residences."""
        self.expect_visible(self.project_locators.Elire.RESIDENCES_BUTTON)
        self.click(self.project_locators.Elire.RESIDENCES_BUTTON)

    def click_on_residences_button_and_request_viewing_form(self):
        """Кликнуть на кнопку Residences и открыть форму Request Viewing."""
        self.expect_visible(self.project_locators.Elire.RESIDENCES_BUTTON)
        self.click(self.project_locators.Elire.RESIDENCES_BUTTON)
        self.click(self.project_locators.Elire.REQUEST_VIEWING_BUTTON)
