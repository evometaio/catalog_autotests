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
            project_name = getattr(self.locators, "PROJECT_NAME", "").lower()
            import os

            device = os.getenv("MOBILE_DEVICE", "desktop")

            # Для MARK на мобилке используем XPath локатор
            if project_name == "mark" and device != "desktop":
                button = self.page.locator(
                    'xpath=(//button[@data-test-id="nav-rotation-view-controls-button"])[2]'
                )
                button.wait_for(state="visible", timeout=10000)
                button.click()
            else:
                # Десктопный или другой проект
                locator = self.page.locator(self.locators.AREA_TOUR_360_BUTTON)
                if project_name == "mark" and locator.count() > 1:
                    # Ищем первую видимую кнопку
                    button = None
                    for idx in range(locator.count()):
                        candidate = locator.nth(idx)
                        try:
                            if candidate.is_visible():
                                button = candidate
                                break
                        except Exception:
                            continue

                    # Если видимая не найдена, берём последнюю
                    if button is None:
                        button = locator.last

                    button.click(force=True)
                else:
                    button = locator.first
                    button.wait_for(state="visible", timeout=10000)
                    button.click()

    def click_360_menu_item(self, menu_item: str = "yard"):
        """
        Кликнуть на пункт меню панорам (для MARK и других проектов с меню выбора).

        Args:
            menu_item: Тип панорамы - "rotation", "yard", "lobby-k1", "lobby-k2", "lobby-k3"
        """
        with allure.step(f"Кликаем на пункт меню панорам: {menu_item}"):
            import os

            device = os.getenv("MOBILE_DEVICE", "desktop")
            project_name = getattr(self.locators, "PROJECT_NAME", "").lower()

            # Проверяем, есть ли специальные локаторы для меню
            if hasattr(self.locators, "AREA_TOUR_360_MENU_TOUR_YARD"):
                # MARK имеет меню выбора
                # На мобилке используется формат nav-rotation-view-controls-list-tour-*
                # На десктопе используется формат nav-rotation-view-controls-menu-*
                if project_name == "mark" and device != "desktop":
                    # Мобильные локаторы
                    mobile_menu_selectors = {
                        "rotation": '[data-test-id="nav-rotation-view-controls-list-tour-rotation"]',
                        "yard": '[data-test-id="nav-rotation-view-controls-list-tour-yard"]',
                        "lobby-k1": '[data-test-id="nav-rotation-view-controls-list-tour-lobby-k1"]',
                        "lobby-k2": '[data-test-id="nav-rotation-view-controls-list-tour-lobby-k2"]',
                        "lobby-k3": '[data-test-id="nav-rotation-view-controls-list-tour-lobby-k3"]',
                    }
                    selector = mobile_menu_selectors.get(menu_item)
                else:
                    # Десктопные локаторы
                    menu_selectors = {
                        "rotation": getattr(
                            self.locators, "AREA_TOUR_360_MENU_ROTATION", None
                        ),
                        "yard": getattr(
                            self.locators, "AREA_TOUR_360_MENU_TOUR_YARD", None
                        ),
                        "lobby-k1": getattr(
                            self.locators, "AREA_TOUR_360_MENU_TOUR_LOBBY_K1", None
                        ),
                        "lobby-k2": getattr(
                            self.locators, "AREA_TOUR_360_MENU_TOUR_LOBBY_K2", None
                        ),
                        "lobby-k3": getattr(
                            self.locators, "AREA_TOUR_360_MENU_TOUR_LOBBY_K3", None
                        ),
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
            assert (
                modal.first.is_visible()
            ), "Модальное окно 360 Area Tour не отображается"

    def verify_content(self):
        """Проверить наличие контента в модальном окне 360 Area Tour."""
        with allure.step("Проверяем наличие контента 360 Area Tour"):
            # Проверяем наличие контента (изображения, видео или другие элементы)
            # Увеличенный таймаут для мобильных устройств в CI (30 секунд)
            content_element = self.page.locator(self.locators.AREA_TOUR_360_CONTENT)
            content_element.first.wait_for(state="attached", timeout=30000)
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
