from core.base_page import BasePage
from locators import locators
from locators import locators


class CapstonePages(BasePage):
    """Класс для работы со страницами Capstone проектов (Peylaa)."""

    def __init__(self, page, url: str = None):
        """Инициализация CapstonePages.

        Args:
            page: Playwright page объект
            url: URL страницы (если не указан, будет использован Capstone map URL)
        """
        if url is None:
            from config.environments import environment_manager

            env_config = environment_manager.get_environment()
            url = env_config.capstone_map_url

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
        from config.environments import environment_manager

        env_config = environment_manager.get_environment()
        project_name_lower = project_name.lower()

        if project_name_lower not in ["peylaa"]:
            raise ValueError(f"Неизвестный Capstone проект: {project_name}")

        base_url = env_config.capstone_map_url.replace("/map", "")

        if page_type == "area":
            return f"{base_url}/project/{project_name_lower}/area"
        elif page_type == "map":
            return env_config.capstone_map_url
        else:
            raise ValueError(f"Неизвестный тип страницы для Capstone: {page_type}")

    def click_project_on_map(self, project_name: str):
        """Кликнуть на проект и затем на кнопку Explore Project."""
        # Используем полную логику из BasePage
        self.wait_for_map_and_projects_loaded()
        # Сначала кликаем на проект
        self.click_project(project_name)

        # Для остальных случаев ищем кнопку Explore Project
        self.expect_visible(self.locators.PROJECT_INFO_WINDOW)

        # Затем кликаем на кнопку Explore Project
        self.click(self.locators.EXPLORE_PROJECT_BUTTON)

        # Ждем изменения URL (универсально для всех типов страниц)
        self.page.wait_for_url(self.locators.PROJECT_URL_PATTERN, timeout=10000)
