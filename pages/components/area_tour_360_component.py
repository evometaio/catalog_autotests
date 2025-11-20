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

    def click_360_menu_item(self, menu_item: str = "yard"):
        """
        Кликнуть на пункт меню панорам (для MARK и других проектов с меню выбора).
        
        Args:
            menu_item: Тип панорамы - "rotation", "yard", "lobby-k1", "lobby-k2", "lobby-k3"
        """
        with allure.step(f"Кликаем на пункт меню панорам: {menu_item}"):
            # Проверяем, есть ли специальные локаторы для меню
            if hasattr(self.locators, "AREA_TOUR_360_MENU_TOUR_YARD"):
                # MARK имеет меню выбора
                menu_selectors = {
                    "rotation": getattr(self.locators, "AREA_TOUR_360_MENU_ROTATION", None),
                    "yard": getattr(self.locators, "AREA_TOUR_360_MENU_TOUR_YARD", None),
                    "lobby-k1": getattr(self.locators, "AREA_TOUR_360_MENU_TOUR_LOBBY_K1", None),
                    "lobby-k2": getattr(self.locators, "AREA_TOUR_360_MENU_TOUR_LOBBY_K2", None),
                    "lobby-k3": getattr(self.locators, "AREA_TOUR_360_MENU_TOUR_LOBBY_K3", None),
                }
                
                selector = menu_selectors.get(menu_item)
                if selector:
                    menu_item_element = self.page.locator(selector)
                    menu_item_element.wait_for(state="visible", timeout=10000)
                    menu_item_element.click()
                else:
                    raise ValueError(f"Неизвестный пункт меню: {menu_item}")
            else:
                # Для других проектов без меню выбора просто кликаем на кнопку
                self.click_360_button()

    def verify_modal_displayed(self):
        """Проверить отображение модального окна 360 Area Tour."""
        with allure.step("Проверяем отображение модального окна 360 Area Tour"):
            modal = self.page.locator(self.locators.AREA_TOUR_360_MODAL)
            modal.first.wait_for(state="visible", timeout=10000)
            assert modal.first.is_visible(), "Модальное окно 360 Area Tour не отображается"

    def verify_content(self):
        """Проверить наличие контента в модальном окне 360 Area Tour."""
        with allure.step("Проверяем наличие контента 360 Area Tour"):
            # Проверяем наличие контента (изображения, видео или другие элементы)
            content_element = self.page.locator(self.locators.AREA_TOUR_360_CONTENT)
            content_element.first.wait_for(state="attached", timeout=10000)
            assert (
                content_element.count() > 0
            ), "Контент 360 Area Tour не найден в модальном окне"

    def close_modal(self):
        """Закрыть модальное окно 360 Area Tour."""
        with allure.step("Закрываем модальное окно 360 Area Tour"):
            # Ищем кнопку закрытия модального окна
            close_button = self.page.locator(self.locators.AREA_TOUR_360_CLOSE_BUTTON)
            if close_button.count() > 0 and close_button.first.is_visible():
                close_button.first.click()
            else:
                # Если кнопки закрытия нет, нажимаем Escape
                self.page.keyboard.press("Escape")

            # Ждем закрытия модального окна
            modal = self.page.locator(self.locators.AREA_TOUR_360_MODAL)
            modal.first.wait_for(state="hidden", timeout=5000)
