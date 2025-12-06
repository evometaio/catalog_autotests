"""Страница проекта Elire."""

import allure
from playwright.sync_api import Page

from locators.qube.elire_locators import ElireLocators

from .qube_base_page import QubeBasePage


class ElirePage(QubeBasePage):
    """
    Страница проекта Elire.

    Наследует от QubeBasePage и добавляет специфичную функциональность Elire.
    """

    def __init__(self, page: Page, url: str = None):
        """
        Инициализация Elire страницы.

        Args:
            page: Playwright Page объект
            url: URL страницы
        """
        # Инициализируем с project_name="elire" и новыми локаторами
        super().__init__(page, "elire", url, ElireLocators)

    # ==================== СПЕЦИФИЧНЫЕ МЕТОДЫ ELIRE ====================

    def click_residences_button(self):
        """Кликнуть на кнопку Residences (специфично для Elire)."""
        with allure.step("Кликаем на Residences"):
            self.browser.click(self.project_locators.RESIDENCES_BUTTON)

    def open_request_viewing_form(self):
        """Открыть форму Request Viewing (специфично для Elire)."""
        with allure.step("Открываем форму Request Viewing"):
            # На проде нужен [2], на деве - первый видимый. Ищем видимую кнопку
            buttons = self.page.locator(self.project_locators.REQUEST_VIEWING_BUTTON)
            button_count = buttons.count()

            # Пробуем найти видимую кнопку
            visible_button = None
            for i in range(button_count):
                button = buttons.nth(i)
                if button.is_visible(timeout=1000):
                    visible_button = button
                    break

            # Если видимая не найдена, пробуем второй элемент (для прода)
            if visible_button is None and button_count >= 2:
                visible_button = buttons.nth(1)

            # Если все еще не найдена, используем первый
            if visible_button is None:
                visible_button = buttons.first

            visible_button.wait_for(state="visible", timeout=10000)
            visible_button.click()

    def fill_request_viewing_form(self, fake):
        """
        Заполнить форму Request Viewing.

        Args:
            fake: Faker объект для генерации данных
        """
        with allure.step("Заполняем форму Request Viewing"):
            self.browser.fill(self.project_locators.FIRST_NAME_FIELD, fake.first_name())
            self.browser.fill(self.project_locators.LAST_NAME_FIELD, fake.last_name())
            self.browser.fill(self.project_locators.PHONE_FIELD, "+79999999999")
            self.browser.fill(self.project_locators.EMAIL_FIELD, fake.email())
            self.browser.fill(self.project_locators.NOTE_FIELD, fake.text())

    def submit_request_viewing_form(self):
        """Отправить форму Request Viewing."""
        with allure.step("Отправляем форму"):
            self.browser.click(self.project_locators.SUBMIT_BUTTON_FOR_REQUEST_VIEWING)

    def verify_success_message(self):
        """Проверить сообщение об успешной отправке."""
        with allure.step("Проверяем сообщение об успехе"):
            self.assertions.assert_element_visible(
                self.project_locators.SUCCESS_MODAL,
                "Модальное окно успеха не отображается",
            )

            # Проверяем текст
            modal = self.page.locator(self.project_locators.SUCCESS_MODAL)
            modal_text = modal.text_content()

            assert (
                "Thank you!" in modal_text
            ), "Текст 'Thank you!' не найден в модальном окне"
            assert (
                "Our specialist will contact you shortly." in modal_text
            ), "Текст подтверждения не найден в модальном окне"

    def click_start_3d_expansion_button(self):
        """Кликнуть на кнопку Start 3D Expansion."""
        with allure.step("Кликаем на Start 3D Expansion"):
            self.browser.click(self.project_locators.START_3D_EXPANSION_BUTTON)

    def click_services_amenities_button(self):
        """Кликнуть на кнопку Services & Amenities."""
        with allure.step("Кликаем на Services & Amenities"):
            self.browser.click(self.project_locators.SERVICES_AMENITIES_BUTTON)

    def click_residences_button_and_request_viewing_form(self):
        """Кликнуть на Residences и открыть форму Request Viewing."""
        self.click_residences_button()
        self.open_request_viewing_form()

    def fill_and_submit_request_viewing_form(self, fake):
        """Заполнить и отправить форму Request Viewing."""
        self.fill_request_viewing_form(fake)
        self.submit_request_viewing_form()

    def is_success_message_displayed(self) -> bool:
        """Проверить отображается ли сообщение об успехе."""
        return self.browser.is_visible(self.project_locators.SUCCESS_MODAL)
