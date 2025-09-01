from playwright.sync_api import Page

from locators.map_locators import MapLocators
from locators.project_locators import QubePageLocators
from pages.base_page import BasePage


class MapPage(BasePage):
    """Класс для работы со страницей карты."""

    def __init__(self, page: Page, base_url: str = None):
        super().__init__(page, base_url)
        self.locators = MapLocators()

        # URL-ы теперь определяются в conftest.py
        self.project_url_template = base_url.replace("/map", "/project/{project}/area")
        self.map_url = base_url

    def open_map_page(self):
        """Открыть страницу карты."""
        self.open()
        self.wait_for_page_load()

        # Убеждаемся, что окно имеет правильный размер
        self.ensure_proper_window_size()

        # Дополнительное ожидание загрузки карты и проектов
        self.wait_for_map_and_projects_loaded()

    def ensure_proper_window_size(self):
        """Обеспечиваем правильный размер окна для лучшей видимости карты."""
        try:
            # Проверяем текущий размер viewport
            current_size = self.page.viewport_size
            if current_size and (
                current_size["width"] < 1920 or current_size["height"] < 1080
            ):
                # Устанавливаем Full HD размер
                self.page.set_viewport_size({"width": 1920, "height": 1080})
        except Exception as e:
            print(e)

    def check_map_loaded(self):
        """Проверить загрузку карты."""
        self.expect_visible(self.locators.MAP_CONTAINER)

    def check_all_projects_visible(self):
        """Проверить видимость всех проектов Qube."""
        projects = self.page.locator(self.locators.ALL_PROJECTS).all()
        expected_count = len(QubePageLocators.ALL_PROJECTS)
        assert (
            len(projects) == expected_count
        ), f"Ожидалось {expected_count} проектов Qube, найдено {len(projects)}"

    def click_project(self, project_name: str):
        """Кликнуть по проекту на карте."""
        # Находим проект по имени
        project = None
        for p in QubePageLocators.ALL_PROJECTS:
            if p.PROJECT_NAME == project_name.lower():
                project = p
                break

        if not project:
            available_projects = [p.PROJECT_NAME for p in QubePageLocators.ALL_PROJECTS]
            raise ValueError(
                f"Неизвестный проект Qube: {project_name}. Доступные: {available_projects}"
            )

        selector = project.MAP_LOCATOR

        # Дополнительная проверка, что проект действительно видим
        try:
            # Ждем появления конкретного проекта
            self.page.wait_for_selector(selector, state="visible", timeout=30000)

            # Дополнительная пауза для стабилизации
            self.page.wait_for_timeout(1000)

        except Exception as e:
            print(f"Проект {project_name} не найден: {e}")

        self.click(selector)

    def check_project_info_visible(self, project_name: str):
        """Проверить видимость информации о проекте."""
        self.expect_visible(self.locators.PROJECT_INFO_WINDOW)

    def open_project_page(self, project_name: str):
        """Открыть страницу проекта."""
        # Находим проект по имени
        project = None
        for p in QubePageLocators.ALL_PROJECTS:
            if p.PROJECT_NAME == project_name.lower():
                project = p
                break

        if not project:
            available_projects = [p.PROJECT_NAME for p in QubePageLocators.ALL_PROJECTS]
            raise ValueError(
                f"Неизвестный проект Qube: {project_name}. Доступные: {available_projects}"
            )

        project_url = self.project_url_template.format(project=project.PROJECT_NAME)
        self.page.goto(project_url)
        self.wait_for_page_load()

    def check_project_page_loaded(self, project_name: str):
        """Проверить загрузку страницы проекта."""
        # Находим проект по имени
        project = None
        for p in QubePageLocators.ALL_PROJECTS:
            if p.PROJECT_NAME == project_name.lower():
                project = p
                break

        if not project:
            raise ValueError(f"Неизвестный проект Qube: {project_name}")

        # Проверяем, что мы на странице проекта (URL содержит /project/ и название проекта)
        self.wait_for_page_load()
        current_url = self.page.url
        self.wait_for_page_load()
        assert (
            f"/project/{project.PROJECT_NAME}" in current_url
        ), f"Не на странице проекта {project.PROJECT_DISPLAY_NAME}. Текущий URL: {current_url}"

    def return_to_map_from_project(self):
        """Вернуться на карту со страницы проекта."""
        self.page.goto(self.map_url)
        self.wait_for_page_load()

    def verify_returned_to_map(self):
        """Проверить, что вернулись на карту."""
        current_url = self.page.url
        assert (
            self.map_url in current_url
        ), f"Не вернулись на карту. Текущий URL: {current_url}"

    def toggle_fullscreen(self):
        """Переключить полноэкранный режим."""
        try:
            # Сначала пробуем основной локатор
            if self.is_visible(self.locators.FULLSCREEN_BUTTON, timeout=5000):
                self.click(self.locators.FULLSCREEN_BUTTON)
            else:
                # Пробуем альтернативные локаторы
                self.click(self.locators.FULLSCREEN_ALT)
        except Exception:
            # Если не удалось, просто логируем
            print("Кнопка полноэкранного режима не найдена или недоступна")
