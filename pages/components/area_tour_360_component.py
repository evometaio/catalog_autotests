"""Компонент для работы с 360 Area Tour."""

import allure
from playwright.sync_api import Page


class AreaTour360Component:
    """
    Компонент 360 Area Tour.

    Ответственность:
    - Открытие модального окна 360 тура
    - Проверка контента
    - Закрытие модального окна
    """

    def __init__(self, page: Page, project_locators):
        """
        Инициализация компонента 360 тура.

        Args:
            page: Playwright Page объект
            project_locators: Локаторы проекта
        """
        self.page = page
        self.locators = project_locators

    def click_360_button(self):
        """Кликнуть на кнопку 360 Area Tour."""
        with allure.step("Кликаем на кнопку 360 Area Tour"):
            button = self.page.locator(self.locators.AREA_TOUR_360_BUTTON)
            button.wait_for(state="visible", timeout=10000)
            button.click()

    def verify_modal_displayed(self):
        """Проверить отображение модального окна 360 Area Tour."""
        with allure.step("Проверяем отображение модального окна 360 Area Tour"):
            modal = self.page.locator(self.locators.AREA_TOUR_360_MODAL)
            modal.wait_for(state="visible", timeout=10000)
            assert modal.is_visible(), "Модальное окно 360 Area Tour не отображается"

    def verify_content(self):
        """Проверить наличие контента в модальном окне 360 Area Tour."""
        with allure.step("Проверяем наличие контента 360 Area Tour"):
            # Проверяем наличие контента (изображения, видео или другие элементы)
            content_element = self.page.locator(self.locators.AREA_TOUR_360_CONTENT)
            assert (
                content_element.count() > 0
            ), "Контент 360 Area Tour не найден в модальном окне"

    def close_modal(self):
        """Закрыть модальное окно 360 Area Tour."""
        with allure.step("Закрываем модальное окно 360 Area Tour"):
            # Ищем кнопку закрытия модального окна
            close_button = self.page.locator(self.locators.AREA_TOUR_360_CLOSE_BUTTON)
            if close_button.is_visible():
                close_button.click()
            else:
                # Если кнопки закрытия нет, нажимаем Escape
                self.page.keyboard.press("Escape")

            # Ждем закрытия модального окна
            modal = self.page.locator(self.locators.AREA_TOUR_360_MODAL)
            modal.wait_for(state="hidden", timeout=5000)
