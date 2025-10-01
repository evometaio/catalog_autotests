"""
Page Object для карт Qube проектов.
"""

from typing import Optional

from core.base_page import BasePage
from locators import locators
from locators import locators


class QubeMapPage(BasePage):
    """Page Object для карт Qube проектов."""

    def __init__(self, page, base_url: str):
        """Инициализация QubeMapPage."""
        super().__init__(page, base_url, QubeLocators)
        # Добавляем локаторы карты
        self.map_locators = MapLocators()

    def click_project_on_map(self, project_name: str) -> None:
        """Кликнуть по проекту на карте и затем на кнопку Explore Project."""
        # Определяем локатор для конкретного проекта
        if project_name.lower() == "arisha":
            selector = locators.get("MAP_LOCATOR")
        elif project_name.lower() == "elire":
            selector = locators.get("MAP_LOCATOR")
        elif project_name.lower() == "cubix":
            selector = locators.get("MAP_LOCATOR")
        else:
            raise ValueError(f"Неизвестный проект: {project_name}")

        # Кликаем на проект
        self.click(selector)

        # Ждем появления информации о проекте (используем первый элемент)
        project_info = self.page.locator('[class*="project"]').first
        project_info.wait_for(state="visible", timeout=10000)

        # Кликаем на кнопку "Explore Project" (десктопная версия)
        self.click(self.map_locators.EXPLORE_PROJECT_BUTTON)

    def click_360_area_tour_button(self) -> None:
        """Кликнуть на кнопку 360 Area Tour."""
        self.click(locators.get("AREA_TOUR_360_BUTTON"))

    def verify_360_area_tour_modal_displayed(self) -> None:
        """Проверить отображение модального окна 360 Area Tour."""
        self.expect_visible(locators.get("AREA_TOUR_360_MODAL"))

    def verify_360_area_tour_content(self) -> None:
        """Проверить наличие контента в модальном окне."""
        # Используем .first для обхода strict mode violation
        content_selector = locators.get("AREA_TOUR_360_CONTENT")
        content_element = self.page.locator(content_selector).first
        content_element.wait_for(state="visible", timeout=10000)

    def close_360_area_tour_modal(self) -> None:
        """Закрыть модальное окно 360 Area Tour."""
        self.click(locators.get("AREA_TOUR_360_CLOSE_BUTTON"))

    def click_project(self, project_name: str) -> None:
        """Алиас для click_project_on_map."""
        self.click_project_on_map(project_name)

    def check_project_info_visible(self, project_name: str) -> None:
        """Проверить видимость информации о проекте."""
        self.expect_visible('[class*="project"]')

    def check_map_loaded(self) -> None:
        """Проверить загрузку карты."""
        self.expect_visible('[class*="map"]')
