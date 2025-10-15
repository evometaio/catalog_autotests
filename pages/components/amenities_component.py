"""Компонент для работы с Explore Amenities."""

import allure
from playwright.sync_api import Page


class AmenitiesComponent:
    """
    Компонент Amenities.

    Ответственность:
    - Открытие модального окна amenities
    - Навигация по слайдеру
    - Проверки отображения
    """

    def __init__(self, page: Page, project_locators):
        """
        Инициализация компонента amenities.

        Args:
            page: Playwright Page объект
            project_locators: Локаторы проекта
        """
        self.page = page
        self.locators = project_locators

    def click_explore_button(self):
        """Открыть модальное окно Explore Amenities."""
        with allure.step("Кликаем на Explore Amenities"):
            button = self.page.locator(self.locators.EXPLORE_AMENITIES_BUTTON)
            button.wait_for(state="visible", timeout=10000)
            button.click()

    def verify_modal_displayed(self):
        """Проверить отображение модального окна."""
        with allure.step("Проверяем отображение модального окна amenities"):
            modal = self.page.locator(self.locators.AMENITIES_MODAL)
            modal.wait_for(state="visible", timeout=10000)
            assert modal.is_visible(), "Модальное окно amenities не отображается"

    def verify_modal_title(self):
        """Проверить наличие заголовка модального окна."""
        with allure.step("Проверяем наличие заголовка"):
            title = self.page.locator(self.locators.AMENITIES_MODAL_TITLE)
            title.wait_for(state="visible", timeout=10000)
            assert title.is_visible(), "Заголовок модального окна не найден"

    def verify_modal_close_button(self):
        """Проверить наличие кнопки закрытия."""
        with allure.step("Проверяем наличие кнопки закрытия"):
            close_button = self.page.locator(self.locators.AMENITIES_MODAL_CLOSE_BUTTON)
            close_button.wait_for(state="visible", timeout=10000)
            assert close_button.is_visible(), "Кнопка закрытия не найдена"

    def verify_slider_displayed(self):
        """Проверить отображение слайдера."""
        with allure.step("Проверяем отображение слайдера"):
            slider = self.page.locator(self.locators.AMENITIES_SLIDER)
            slider.wait_for(state="visible", timeout=10000)
            assert slider.is_visible(), "Слайдер amenities не отображается"

    def verify_slider_images(self):
        """Проверить наличие изображений в слайдере."""
        with allure.step("Проверяем наличие изображений в слайдере"):
            images = self.page.locator(self.locators.AMENITIES_SLIDER_IMAGES)
            count = images.count()
            assert count > 0, "Изображения в слайдере amenities не найдены"
            return count

    def verify_slider_indicators(self):
        """Проверить наличие индикаторов слайдера."""
        with allure.step("Проверяем наличие индикаторов"):
            indicators = self.page.locator(self.locators.AMENITIES_SLIDER_INDICATORS)
            count = indicators.count()
            assert count > 0, "Индикаторы слайдера amenities не найдены"
            return count

    def navigate_slider(self, direction: str, count: int = 1):
        """
        Навигация по слайдеру.

        Args:
            direction: Направление ("next" или "prev")
            count: Количество кликов
        """
        with allure.step(f"Навигация по слайдеру: {direction} ({count} раз)"):
            if direction == "next":
                selector = self.locators.AMENITIES_SLIDER_NEXT_BUTTON
            else:
                selector = self.locators.AMENITIES_SLIDER_PREV_BUTTON

            button = self.page.locator(selector)

            for i in range(count):
                button.click()
                self.page.wait_for_timeout(800)

    def click_indicator(self, index: int):
        """
        Кликнуть на индикатор слайдера.

        Args:
            index: Индекс индикатора (0-based)
        """
        with allure.step(f"Кликаем на индикатор #{index + 1}"):
            indicators = self.page.locator(self.locators.AMENITIES_SLIDER_INDICATORS)
            indicators.nth(index).click()
            self.page.wait_for_timeout(800)

    def click_slider_next(self):
        """Кликнуть на кнопку 'следующий'."""
        self.navigate_slider("next", 1)

    def click_slider_prev(self):
        """Кликнуть на кнопку 'предыдущий'."""
        self.navigate_slider("prev", 1)

    def close_modal(self):
        """Закрыть модальное окно."""
        with allure.step("Закрываем модальное окно amenities"):
            close_button = self.page.locator(self.locators.AMENITIES_MODAL_CLOSE_BUTTON)
            close_button.click()

            # Ждем закрытия
            modal = self.page.locator(self.locators.AMENITIES_MODAL)
            modal.wait_for(state="hidden", timeout=5000)

    def verify_modal_closed(self):
        """Проверить что модальное окно закрыто."""
        with allure.step("Проверяем что модальное окно закрылось"):
            modal = self.page.locator(self.locators.AMENITIES_MODAL)
            modal.wait_for(state="hidden", timeout=5000)
