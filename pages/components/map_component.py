"""Компонент для работы с картой."""

import allure
from playwright.sync_api import Page
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

from locators.map_locators import MapLocators


class MapComponent:
    """
    Компонент карты.

    Ответственность:
    - Загрузка карты
    - Клик по проектам на карте
    - Навигация к проектам
    """

    MAP_LOAD_TIMEOUT = 20000

    def __init__(self, page: Page, project_locators):
        """
        Инициализация компонента карты.

        Args:
            page: Playwright Page объект
            project_locators: Локаторы проекта
        """
        self.page = page
        self.project_locators = project_locators
        self.locators = MapLocators()

    def wait_for_map_loaded(self):
        """Ожидать загрузки карты и проектов."""
        with allure.step("Ожидаем загрузки карты"):
            try:
                # Ждем контейнера карты
                self.page.wait_for_selector(
                    self.locators.MAP_CONTAINER,
                    state="visible",
                    timeout=self.MAP_LOAD_TIMEOUT,
                )

                # Ждем появления проектов
                self.page.wait_for_selector(
                    self.locators.ALL_PROJECTS_SELECTOR,
                    state="visible",
                    timeout=self.MAP_LOAD_TIMEOUT,
                )

                # Пауза для стабилизации
                self.page.wait_for_timeout(2000)
            except Exception as e:
                print(f"Ошибка при ожидании загрузки карты: {e}")

    def check_map_loaded(self):
        """Проверить что карта загружена."""
        element = self.page.locator(self.locators.MAP_CONTAINER)
        try:
            element.wait_for(state="visible", timeout=self.MAP_LOAD_TIMEOUT)
        except PlaywrightTimeoutError:
            raise AssertionError(f"Карта не загружена за {self.MAP_LOAD_TIMEOUT}ms.")
        assert element.is_visible(), "Карта не загружена"

    def click_project(self, project_name: str):
        """
        Кликнуть по проекту на карте.

        Args:
            project_name: Название проекта (arisha, elire, etc.)
        """
        with allure.step(f"Кликаем на проект {project_name.upper()}"):
            selector = self._get_project_selector(project_name)

            # Ждем появления проекта
            try:
                self.page.wait_for_selector(selector, state="visible", timeout=20000)
            except PlaywrightTimeoutError:
                raise AssertionError(
                    f"Проект '{project_name}' не найден на карте за 20000ms."
                )

            # Для изображений на карте используем force_click
            if project_name.lower() == "peylaa" and "img" in selector:
                element = self.page.locator(selector)
                element.click(force=True)
            elif project_name.lower() == "edgewater":
                # Для edgewater используем force_click, так как на карте могут быть проблемы с кликом
                element = self.page.locator(selector).first
                element.click(force=True)
            else:
                element = self.page.locator(selector)
                element.click()

    def click_explore_project(self, project_name: str):
        """
        Кликнуть на кнопку Explore Project.

        Args:
            project_name: Название проекта
        """
        with allure.step(f"Кликаем на Explore Project для {project_name.upper()}"):
            # Получаем селектор кнопки
            button_selector = self._get_explore_button_selector(project_name)

            # Best-effort: on some maps (e.g. mobile layouts) project info window markup differs,
            # so do not hard-fail on PROJECT_INFO_WINDOW. We only need Explore button to appear.
            try:
                self.page.wait_for_selector(
                    self.locators.PROJECT_INFO_WINDOW, state="visible", timeout=5000
                )
            except PlaywrightTimeoutError:
                pass

            # Ждем появления кнопки и проверяем её готовность
            button = self.page.locator(button_selector)
            try:
                button.wait_for(state="visible", timeout=20000)
            except PlaywrightTimeoutError:
                raise AssertionError(
                    f"Кнопка Explore Project для {project_name} не найдена за 20000ms."
                )

            assert (
                button.is_enabled()
            ), f"Кнопка Explore Project заблокирована для {project_name} - баг в UI"

            button.click()

            # Ждем перехода на страницу проекта
            try:
                self.page.wait_for_url(
                    self.project_locators.PROJECT_URL_PATTERN,
                    wait_until="domcontentloaded",
                    timeout=20000,
                )
            except PlaywrightTimeoutError:
                raise AssertionError(
                    f"Не перешли на страницу проекта {project_name} за 20000ms. Текущий URL: {self.page.url}"
                )

    def click_on_custom_poi(self):
        """Кликнуть на кастомную POI."""
        self.page.locator(self.locators.POI_LOCATOR).click()

    def navigate_to_project(self, project_name: str):
        """
        Полная навигация: загрузка карты -> клик на проект -> Explore.

        Args:
            project_name: Название проекта
        """
        with allure.step(f"Навигация к проекту {project_name.upper()}"):
            self.wait_for_map_loaded()
            self.click_project(project_name)
            self.click_explore_project(project_name)

    def check_project_info_visible(self, project_name: str):
        """
        Проверить видимость информационного окна проекта.

        Args:
            project_name: Название проекта
        """
        element = self.page.locator(self.locators.PROJECT_INFO_WINDOW)
        try:
            element.wait_for(state="visible", timeout=20000)
        except PlaywrightTimeoutError:
            raise AssertionError(
                f"Информационное окно проекта {project_name} не отображается за 20000ms."
            )
        assert (
            element.is_visible()
        ), f"Информационное окно проекта {project_name} не отображается"

    def check_project_page_loaded(self, project_name: str):
        """
        Проверить что страница проекта загружена.

        Args:
            project_name: Название проекта
        """
        # Находим проект по имени
        project = None
        for p in self.project_locators.ALL_PROJECTS:
            if p.PROJECT_NAME == project_name.lower():
                project = p
                break

        if not project:
            raise ValueError(f"Неизвестный проект: {project_name}")

        # Проверяем URL
        current_url = self.page.url
        self.page.wait_for_load_state("domcontentloaded")
        assert (
            f"/project/{project.PROJECT_NAME}" in current_url
        ), f"Не на странице проекта {project.PROJECT_DISPLAY_NAME}. Текущий URL: {current_url}"

    def return_to_map_from_project(self):
        """Вернуться на карту из проекта."""
        self.page.go_back()
        self.check_map_loaded()

    def _get_project_selector(self, project_name: str) -> str:
        """Получить селектор проекта."""
        import os

        project_name_lower = project_name.lower()
        device = os.getenv("MOBILE_DEVICE", "desktop")

        # Мапинг проектов на селекторы
        if device != "desktop":
            # Мобильные селекторы
            selectors = {
                "arisha": 'div[aria-label="ARISHA TERACCES"]',
                "elire": 'div[aria-label="Elire"]',
                "cubix": 'div[aria-label="CUBIX RESIDENCE"], div[aria-label="CUBIX RESIDENCES"]',
                "tranquil": 'div[aria-label="Tranquil Wellness Tower"]',
                "peylaa": 'div[aria-label="Peylaa"]',
                "edgewater": 'div[aria-label*="Edgewater Residences"]',
                "willows_residences": 'div[aria-label="Willows Residences"]',
            }
        else:
            # Десктопные селекторы
            selectors = {
                "arisha": 'div[aria-label="ARISHA TERRACES"]',
                "elire": 'div[aria-label="Elire"]',
                "cubix": 'div[aria-label="CUBIX RESIDENCE"], div[aria-label="CUBIX RESIDENCES"]',
                "tranquil": 'div[aria-label="Tranquil Wellness Tower"]',
                "peylaa": 'div[aria-label="Peylaa"]',
                "edgewater": 'div[aria-label*="Edgewater Residences"]',
                "willows_residences": 'div[aria-label="Willows Residences"]',
            }

        return selectors.get(
            project_name_lower, f'div[aria-label*="{project_name.upper()}"]'
        )

    def _get_explore_button_selector(self, project_name: str) -> str:
        """Получить селектор кнопки Explore."""
        import os

        project_name_lower = project_name.lower()
        device = os.getenv("MOBILE_DEVICE", "desktop")

        # Специальная обработка для edgewater (на карте есть несколько проектов: edgewater-residences-1, 2, 3)
        if project_name_lower == "edgewater":
            if device != "desktop":
                return '[data-test-id*="map-project-point-button-mobile-edgewater"]'
            else:
                return '[data-test-id*="map-project-point-button-desktop-edgewater"]'

        # Специальная обработка для willows_residences (используется "willows" в data-test-id)
        if project_name_lower == "willows_residences":
            if device != "desktop":
                return '[data-test-id*="map-project-point-button-mobile-willows"]'
            else:
                return '[data-test-id*="map-project-point-button-desktop-willows"]'

        if device != "desktop":
            return (
                f'[data-test-id="map-project-point-button-mobile-{project_name_lower}"]'
            )
        else:
            return f'[data-test-id="map-project-point-button-desktop-{project_name_lower}"]'
