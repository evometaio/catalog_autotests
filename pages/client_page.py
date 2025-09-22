from locators.map_locators import MapLocators
from locators.project_locators import QubePageLocators

from .base_page import BasePage


class ClientPage(BasePage):
    """Page Object для клиентских страниц."""

    def __init__(self, page, url: str):
        """Инициализация ClientPage.

        Args:
            page: Playwright page объект
            url: URL клиентской страницы
        """
        super().__init__(page, url, QubePageLocators)
        self.map_locators = MapLocators()

    def click_on_residences_button_and_request_viewing_form(self):
        """Кликает на кнопку Residences и открывает форму Request Viewing."""
        # Используем QubePages для работы с кнопками
        from .qube.qube_pages import QubePages

        qube_pages = QubePages(self.page, self.base_url)
        qube_pages.click_on_residences_button_and_request_viewing_form()

    def fill_and_submit_request_viewing_form(self, fake):
        """Заполняет форму Request Viewing.

        Args:
            fake: Faker объект для генерации тестовых данных
        """
        self.fill(self.project_locators.Elire.FIRST_NAME_FIELD, fake.first_name())
        self.fill(self.project_locators.Elire.LAST_NAME_FIELD, fake.last_name())
        self.fill(self.project_locators.Elire.PHONE_FIELD, "+79999999999")
        self.fill(self.project_locators.Elire.EMAIL_FIELD, fake.email())
        self.fill(self.project_locators.Elire.NOTE_FIELD, fake.text())
        self.click(self.project_locators.Elire.SUBMIT_BUTTON_FOR_REQUEST_VIEWING)

    def is_success_message_displayed(self) -> bool:
        """
        Проверяет, отображается ли сообщение об успешной отправке.

        Returns:
            bool: True если сообщение об успехе отображается
        """
        # Нужны локаторы для модального окна
        project_locators = QubePageLocators()

        # Проверяем модальное окно
        modal = self.page.locator(project_locators.Elire.SUCCESS_MODAL)

        if modal.is_visible():
            # Получаем весь текст модального окна
            modal_text = modal.text_content()

            # Проверяем наличие нужных текстов
            has_thank_you = "Thank you!" in modal_text
            has_contact_text = "Our specialist will contact you shortly." in modal_text

            if has_thank_you and has_contact_text:
                return True
        return False
