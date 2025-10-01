from core.base_page import BasePage
from locators import locators
from locators import locators


class ClientPage(BasePage):
    """Page Object для клиентских страниц Qube проектов."""

    def __init__(self, page, url: str):
        """Инициализация ClientPage.

        Args:
            page: Playwright page объект
            url: URL клиентской страницы
        """
        super().__init__(page, url, QubeLocators)
        self.map_locators = MapLocators()

    def click_on_residences_button_and_request_viewing_form(self):
        """Кликает на кнопку Residences и открывает форму Request Viewing."""
        # Используем методы из внутреннего класса Elire
        self.elire.click_on_residences_button_and_request_viewing_form()

    def fill_and_submit_request_viewing_form(self, fake):
        """Заполняет форму Request Viewing.

        Args:
            fake: Faker объект для генерации тестовых данных
        """
        self.fill(locators.get("FIRST_NAME_FIELD"), fake.first_name())
        self.fill(locators.get("LAST_NAME_FIELD"), fake.last_name())
        self.fill(locators.get("PHONE_FIELD"), "+79999999999")
        self.fill(locators.get("EMAIL_FIELD"), fake.email())
        self.fill(locators.get("NOTE_FIELD"), fake.text())
        self.click(locators.get("SUBMIT_BUTTON_FOR_REQUEST_VIEWING"))

    def is_success_message_displayed(self) -> bool:
        """
        Проверяет, отображается ли сообщение об успешной отправке.

        Returns:
            bool: True если сообщение об успехе отображается
        """
        # Нужны локаторы для модального окна
        project_locators = self.project_locators

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
