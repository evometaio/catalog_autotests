"""Компонент для работы с Explore Amenities."""

import allure
from playwright.sync_api import Page
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError


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
            buttons = self.page.locator(self.locators.EXPLORE_AMENITIES_BUTTON)
            buttons.first.wait_for(state="attached", timeout=20000)

            # Avoid strict-mode issues if there are duplicates: click first visible.
            clicked = False
            for i in range(buttons.count()):
                b = buttons.nth(i)
                try:
                    if b.is_visible(timeout=500) and b.is_enabled():
                        b.click()
                        clicked = True
                        break
                except Exception:
                    continue

            if not clicked:
                buttons.first.wait_for(state="visible", timeout=20000)
                buttons.first.click()

    def verify_modal_displayed(self):
        """Проверить отображение модального окна."""
        with allure.step("Проверяем отображение модального окна amenities"):
            modal = self.page.locator(self.locators.AMENITIES_MODAL)
            try:
                modal.wait_for(state="visible", timeout=20000)
            except PlaywrightTimeoutError:
                raise AssertionError(
                    "Модальное окно amenities не появилось за 20000ms."
                )
            assert modal.is_visible(), "Модальное окно amenities не отображается"

    def verify_modal_title(self):
        """Проверить наличие заголовка модального окна."""
        with allure.step("Проверяем наличие заголовка"):
            modal = self.page.locator(self.locators.AMENITIES_MODAL)
            modal.wait_for(state="visible", timeout=20000)

            # Prefer semantic headings inside the modal; do not rely on a single fixed selector
            headings = modal.locator("h1, h2, h3, h4, h5, h6")
            if headings.count() > 0:
                first_heading = headings.first
                first_heading.wait_for(state="visible", timeout=20000)
                assert first_heading.is_visible(), "Заголовок модального окна не найден"
                return

            # Fallback: modal should contain some non-empty text
            text = (modal.inner_text(timeout=20000) or "").strip()
            assert text, "Модалка amenities пустая (нет текста/заголовка)"

    def verify_modal_close_button(self):
        """Проверить наличие кнопки закрытия."""
        with allure.step("Проверяем наличие кнопки закрытия"):
            close_button = self.page.locator(self.locators.AMENITIES_MODAL_CLOSE_BUTTON)
            close_button.wait_for(state="visible", timeout=20000)
            assert close_button.is_visible(), "Кнопка закрытия не найдена"

    def verify_slider_displayed(self):
        """Проверить отображение слайдера."""
        with allure.step("Проверяем отображение слайдера"):
            slider = self.page.locator(self.locators.AMENITIES_SLIDER)
            slider.wait_for(state="visible", timeout=20000)
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
