"""Локаторы для проекта Elire."""

from ..base_locators import BaseLocators


class ElireLocators(BaseLocators):
    """Локаторы для проекта Elire."""

    # Основная информация о проекте
    PROJECT_NAME = "elire"
    PROJECT_DISPLAY_NAME = "Elire"
    MAP_LOCATOR = 'div[aria-label="Elire"]'
    
    # Специфичные кнопки Elire
    RESIDENCES_BUTTON = '[data-test-id="nav-desktop-catalog2d"]'
    REQUEST_VIEWING_BUTTON = "(//button[@data-test-id='property-info-secondary-button-1 BEDROOM RESIDENCE'])[2]"
    START_3D_EXPANSION_BUTTON = "//button[contains(text(), 'Start 3D Experience')]"
    SUBMIT_BUTTON_FOR_REQUEST_VIEWING = "(//button[.//span[text()='SUBMIT']])[2]"
    SERVICES_AMENITIES_BUTTON = "//*[@id='PubliczonesPolygon']"
    START3DEXPREINCE_1BEDROOM_RESIDENCE = '(//button[@data-test-id="property-info-primary-button-1 BEDROOM RESIDENCE"])[2]'

    # Локаторы для полей формы Request Viewing
    FIRST_NAME_FIELD = "(//input[@id='first_name'])[2]"
    LAST_NAME_FIELD = "(//input[@id='last_name'])[2]"
    PHONE_FIELD = "(//input[@id='phone'])[2]"
    EMAIL_FIELD = "(//input[@id='email'])[2]"
    NOTE_FIELD = "(//textarea[@id='note'])[2]"

    # Локаторы для модального окна успешной отправки
    SUCCESS_MODAL = 'xpath=(//div[@class="ant-modal-content"])[1]'
    SUCCESS_MODAL_TITLE = 'xpath=.//div[contains(text(), "Thank you!")]'
    SUCCESS_MODAL_TEXT = 'xpath=.//div[contains(text(), "Our specialist will contact you shortly.")]'

