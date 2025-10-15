"""Мобильный компонент для работы с картой."""

import allure
from playwright.sync_api import Page

from locators.mobile_locators import (
    MOBILE_CLOSE_BUTTON,
    MOBILE_EXPLORE_BUTTON,
    MOBILE_MODAL_MASK,
    MOBILE_PROJECT_INFO_MODAL,
)


class MobileMapComponent:
    """
    Мобильный компонент карты.

    Ответственность:
    - Клик по проектам на мобильной карте
    - Работа с мобильными модальными окнами
    - Навигация к проектам на мобильных устройствах
    """

    def __init__(self, page: Page):
        """
        Инициализация мобильного компонента карты.

        Args:
            page: Playwright Page объект
        """
        self.page = page

    def get_mobile_project_selector(self, project_name: str) -> str:
        """Получить мобильный селектор для проекта."""
        from locators.mobile_locators import get_mobile_project_selector

        return get_mobile_project_selector(project_name)

    def click_project(self, project_name: str):
        """
        Кликнуть по проекту на карте для мобильных устройств.

        Args:
            project_name: Название проекта
        """
        with allure.step(f"Кликаем по проекту {project_name.upper()} на мобильном"):
            # Получаем мобильный селектор
            selector = self.get_mobile_project_selector(project_name)

            # Ждем появления проекта на карте
            project_element = self.page.locator(selector)
            project_element.wait_for(state="visible", timeout=10000)

            # Кликаем по проекту
            project_element.click()

            # Ждем появления мобильного модального окна
            self.wait_for_project_modal()

    def wait_for_project_modal(self):
        """Ждать появления мобильного модального окна с информацией о проекте."""
        mobile_modal = self.page.locator(MOBILE_PROJECT_INFO_MODAL)
        mobile_modal.wait_for(state="visible", timeout=10000)

        # Проверяем что модальное окно видимо
        assert mobile_modal.is_visible(), "Мобильное модальное окно не видимо"

    def click_explore_project(self, project_name: str):
        """
        Кликнуть по кнопке Explore Project в мобильном модальном окне.

        Args:
            project_name: Название проекта
        """
        with allure.step(f"Кликаем на Explore Project для {project_name.upper()}"):
            # Ждем появления кнопки
            explore_button = self.page.locator(MOBILE_EXPLORE_BUTTON)
            explore_button.wait_for(state="visible", timeout=10000)

            # Проверяем активность кнопки
            assert (
                explore_button.is_enabled()
            ), f"Кнопка Explore Project заблокирована для {project_name}"

            # Кликаем
            explore_button.click()

            # Ждем перехода на страницу проекта
            expected_url_pattern = f"**/{project_name.lower()}/**"
            self.page.wait_for_url(expected_url_pattern, timeout=10000)

    def navigate_to_project(self, project_name: str):
        """
        Полная навигация от карты до страницы проекта на мобильном.

        Args:
            project_name: Название проекта
        """
        with allure.step(f"Навигация к проекту {project_name.upper()} (мобильная)"):
            self.click_project(project_name)
            self.click_explore_project(project_name)

            # Проверяем успешность перехода
            current_url = self.page.url
            assert (
                f"/{project_name.lower()}/" in current_url
            ), f"Не удалось перейти к проекту {project_name}"

    def close_project_modal(self):
        """Закрыть мобильное модальное окно."""
        close_button = self.page.locator(MOBILE_CLOSE_BUTTON)

        if close_button.count() > 0 and close_button.is_visible():
            close_button.click()
        else:
            # Если нет кнопки закрытия, кликаем по маске
            mask = self.page.locator(MOBILE_MODAL_MASK)
            if mask.is_visible():
                mask.click()
            else:
                # Последний вариант - нажатие Escape
                self.page.keyboard.press("Escape")
