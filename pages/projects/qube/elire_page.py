"""Страница проекта Elire."""

import allure
from playwright.sync_api import Page

from .qube_base_page import QubeBasePage
from locators.qube.elire_locators import ElireLocators


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
            self.browser.click(self.project_locators.REQUEST_VIEWING_BUTTON)

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
                "Модальное окно успеха не отображается"
            )
            
            # Проверяем текст
            modal = self.page.locator(self.project_locators.SUCCESS_MODAL)
            modal_text = modal.text_content()
            
            assert "Thank you!" in modal_text, \
                "Текст 'Thank you!' не найден в модальном окне"
            assert "Our specialist will contact you shortly." in modal_text, \
                "Текст подтверждения не найден в модальном окне"

    def click_start_3d_expansion_button(self):
        """Кликнуть на кнопку Start 3D Expansion."""
        with allure.step("Кликаем на Start 3D Expansion"):
            self.browser.click(self.project_locators.START_3D_EXPANSION_BUTTON)

    def click_services_amenities_button(self):
        """Кликнуть на кнопку Services & Amenities."""
        with allure.step("Кликаем на Services & Amenities"):
            self.browser.click(self.project_locators.SERVICES_AMENITIES_BUTTON)
