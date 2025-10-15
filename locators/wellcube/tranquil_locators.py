"""Локаторы для проекта Tranquil (Wellcube)."""

from ..base_locators import BaseLocators


class TranquilLocators(BaseLocators):
    """Локаторы для проекта Tranquil."""

    # Основная информация о проекте
    PROJECT_NAME = "tranquil"
    PROJECT_DISPLAY_NAME = "Tranquil"
    MAP_LOCATOR = 'div[aria-label*="Tranquil"], div[aria-label*="TRANQUIL"]'
    
    # Специфичные кнопки для Tranquil
    FRACTION_OWNERSHIP_OFFER_BUTTON = '(//button[@data-test-id="property-info-primary-button-1102 A"])[2]'

