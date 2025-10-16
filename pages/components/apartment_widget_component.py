"""Компонент для работы с виджетом апартамента."""

import allure
from playwright.sync_api import Page


class ApartmentWidgetComponent:
    """
    Компонент виджета апартамента.

    Ответственность:
    - Переключение режимов 2D/3D
    - Навигация по слайдам
    - Управление скоростью
    - Проверки отображения
    """

    def __init__(self, page: Page, project_locators, project_name: str = "arisha"):
        """
        Инициализация компонента виджета.

        Args:
            page: Playwright Page объект
            project_locators: Локаторы проекта
            project_name: Название проекта (для получения специфичных локаторов)
        """
        self.page = page
        self.project_name = project_name

        # Получаем локаторы виджета для конкретного проекта
        # project_locators это КЛАСС локаторов (например, ArishaLocators)
        if hasattr(project_locators, "ApartmentWidget"):
            self.locators = project_locators.ApartmentWidget
        else:
            # Fallback на базовые локаторы
            self.locators = None

    def get_widget_frame(self):
        """Получить frame_locator для виджета апартамента."""
        return self.page.frame_locator("iframe[class*='_iframe_']")

    def wait_for_widget_load(self):
        """Ожидать загрузки виджета."""
        with allure.step("Ожидаем загрузки виджета апартамента"):
            # Ждем появления iframe
            self.page.wait_for_selector("iframe[class*='_iframe_']", timeout=15000)

            # Ждем загрузки содержимого iframe
            iframe = self.get_widget_frame()
            iframe.locator("body").wait_for(state="visible", timeout=15000)

            # Дополнительная пауза
            self.page.wait_for_timeout(4000)

    def _close_modal_if_present(self):
        """Закрыть модальное окно, если оно перекрывает виджет (только на client route)."""
        # Проверяем, что мы на client route
        current_url = self.page.url
        if "/client/" not in current_url:
            return  # Модалка появляется только на client route

        try:
            # Проверяем наличие модалки с коротким таймаутом
            modal_close_button = self.page.locator(
                'button[aria-label="Close"].ant-modal-close'
            )
            if modal_close_button.is_visible(timeout=1000):
                with allure.step("Закрываем модальное окно client route"):
                    modal_close_button.click()
                    self.page.wait_for_timeout(1500)
        except Exception:
            # Модалки нет - это нормально
            pass

    def switch_to_2d_mode(self):
        """Переключиться в режим 2D."""
        if not self.locators:
            raise ValueError(
                f"Локаторы виджета не найдены для проекта {self.project_name}"
            )

        # Закрываем модалку если она есть (например, на client route)
        self._close_modal_if_present()

        with allure.step("Переключаемся в режим 2D"):
            frame_locator = self.get_widget_frame()

            view_2d_button = frame_locator.locator(self.locators.VIEW_2D_BUTTON)
            view_2d_button.wait_for(state="visible", timeout=15000)

            # Проверяем, что кнопка 2D не активна
            button_class = view_2d_button.get_attribute("class")
            if "active" in button_class:
                return  # Уже в режиме 2D

            view_2d_button.click()

            # Ждем активации кнопки
            self.page.wait_for_timeout(1000)

            # Ждем появления стрелочек навигации в режиме 2D
            next_arrow = frame_locator.locator(self.locators.NEXT_ARROW).first
            next_arrow.wait_for(state="visible", timeout=10000)

    def switch_to_3d_mode(self):
        """Переключиться в режим 3D."""
        if not self.locators:
            raise ValueError(
                f"Локаторы виджета не найдены для проекта {self.project_name}"
            )

        # Закрываем модалку если она есть (например, на client route)
        self._close_modal_if_present()

        with allure.step("Переключаемся в режим 3D"):
            frame_locator = self.get_widget_frame()

            view_3d_button = frame_locator.locator(self.locators.VIEW_3D_BUTTON)
            view_3d_button.wait_for(state="visible", timeout=15000)

            # Проверяем, что кнопка 3D не активна
            button_class = view_3d_button.get_attribute("class")
            if "active" in button_class:
                return  # Уже в режиме 3D

            view_3d_button.click()

            # Ждем активации кнопки
            self.page.wait_for_timeout(1000)

    def click_speed_button(self) -> bool:
        """
        Кликнуть на кнопку скорости 0.5x.

        Returns:
            bool: True если кнопка была найдена и нажата
        """
        if not self.locators:
            return False

        with allure.step("Кликаем на кнопку скорости"):
            frame_locator = self.get_widget_frame()
            speed_button = frame_locator.locator(self.locators.SPEED_BUTTON)

            if speed_button.count() > 0 and speed_button.first.is_visible():
                speed_button.first.click()
                self.page.wait_for_timeout(500)
                return True
            return False

    def navigate_to_next_slide(self, count: int = 1):
        """
        Перейти к следующему слайду.

        Args:
            count: Количество слайдов для перехода

        Returns:
            list: Список названий сцен после каждого перехода
        """
        if not self.locators:
            raise ValueError(
                f"Локаторы виджета не найдены для проекта {self.project_name}"
            )

        with allure.step(f"Переходим к следующему слайду ({count} раз)"):
            frame_locator = self.get_widget_frame()

            next_arrows = frame_locator.locator(self.locators.NEXT_ARROW)
            scene_indicator = frame_locator.locator(self.locators.SCENE_INDICATOR)

            scenes = []

            for i in range(count):
                if next_arrows.count() > 0:
                    next_arrow = next_arrows.first
                    if next_arrow.is_visible():
                        # Используем JavaScript клик
                        next_arrow.evaluate("element => element.click()")

                        # Пауза для стабилизации
                        self.page.wait_for_timeout(500)

                        # Ждем изменения сцены
                        if scene_indicator.count() > 0:
                            scene_indicator.first.wait_for(
                                state="visible", timeout=2000
                            )

                        # Получаем текущую сцену
                        if scene_indicator.count() > 0:
                            current_scene = scene_indicator.first.text_content()
                            scenes.append(current_scene)

            return scenes

    def get_current_scene(self):
        """
        Получить текущую сцену.

        Returns:
            str: Название текущей сцены или None
        """
        if not self.locators:
            return None

        frame_locator = self.get_widget_frame()
        scene_indicator = frame_locator.locator(self.locators.SCENE_INDICATOR)

        if scene_indicator.count() > 0:
            return scene_indicator.first.text_content()
        return None

    def check_navigation_arrows_visible(self) -> bool:
        """
        Проверить видимость стрелочек навигации.

        Returns:
            bool: True если стрелочки видны
        """
        if not self.locators:
            return False

        frame_locator = self.get_widget_frame()

        prev_arrows = frame_locator.locator(self.locators.PREV_ARROW)
        next_arrows = frame_locator.locator(self.locators.NEXT_ARROW)

        prev_visible = prev_arrows.count() > 0 and prev_arrows.first.is_visible()
        next_visible = next_arrows.count() > 0 and next_arrows.first.is_visible()

        return prev_visible and next_visible

    def check_navigation_arrows_hidden(self) -> bool:
        """
        Проверить, что стрелочки навигации скрыты.

        Returns:
            bool: True если стрелочки скрыты
        """
        if not self.locators:
            return True

        frame_locator = self.get_widget_frame()

        prev_arrows = frame_locator.locator(self.locators.PREV_ARROW)
        next_arrows = frame_locator.locator(self.locators.NEXT_ARROW)

        prev_hidden = prev_arrows.count() == 0 or not prev_arrows.first.is_visible()
        next_hidden = next_arrows.count() == 0 or not next_arrows.first.is_visible()

        return prev_hidden and next_hidden

    def check_mode_button_active(self, mode: str) -> bool:
        """
        Проверить, что кнопка режима активна.

        Args:
            mode: Режим ('2D' или '3D')

        Returns:
            bool: True если кнопка активна
        """
        if not self.locators:
            return False

        frame_locator = self.get_widget_frame()

        if mode == "2D":
            button = frame_locator.locator(self.locators.VIEW_2D_BUTTON)
        elif mode == "3D":
            button = frame_locator.locator(self.locators.VIEW_3D_BUTTON)
        else:
            raise ValueError(f"Неизвестный режим: {mode}")

        button_class = button.get_attribute("class")
        return "active" in button_class if button_class else False

    def take_widget_screenshot(self):
        """
        Сделать скриншот виджета.

        Returns:
            bytes: Скриншот в формате PNG
        """
        iframe_element = self.page.locator("iframe")
        return iframe_element.screenshot()
