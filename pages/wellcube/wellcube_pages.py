from core.base_page import BasePage
from locators import locators
from locators import locators


class WellcubePages(BasePage):
    """Класс для работы со страницами Wellcube проектов (Tranquil)."""

    def __init__(self, page, url: str = None):
        """Инициализация WellcubePages.

        Args:
            page: Playwright page объект
            url: URL страницы (если не указан, будет использован Wellcube map URL)
        """
        if url is None:
            from config.environments import environment_manager

            env_config = environment_manager.get_environment()
            url = env_config.wellcube_map_url

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
        from config.environments import environment_manager

        env_config = environment_manager.get_environment()
        project_name_lower = project_name.lower()

        if project_name_lower not in ["tranquil"]:
            raise ValueError(f"Неизвестный Wellcube проект: {project_name}")

        base_url = env_config.wellcube_map_url.replace("/map", "")

        if page_type == "catalog2d":
            return f"{base_url}/project/{project_name_lower}/catalog_2d"
        elif page_type == "area":
            return f"{base_url}/project/{project_name_lower}/area"
        elif page_type == "map":
            return env_config.wellcube_map_url
        else:
            raise ValueError(f"Неизвестный тип страницы: {page_type}")

    def click_on_fraction_ownership_offer_button(self):
        """Кликнуть на кнопку "Скачать ownership offer"""
        self.click(locators.get("FRACTION_OWNERSHIP_OFFER_BUTTON"))
