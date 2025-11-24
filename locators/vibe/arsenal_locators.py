"""Локаторы для проекта Arsenal (Vibe)."""

from ..base_locators import BaseLocators


class ArsenalLocators(BaseLocators):
    """Локаторы для проекта Arsenal."""

    # Основная информация о проекте
    PROJECT_NAME = "arsenal"
    PROJECT_DISPLAY_NAME = "Arsenal"
    MAP_LOCATOR = 'div[aria-label*="ARSENAL"], div[aria-label*="Arsenal"], div[aria-label*="ARSENAL"]'

    # Каталог квартир
    PROPERTY_INFO_PRIMARY_BUTTON = '[data-test-id^="property-info-primary-button-"]'
    PROPERTY_INFO_SECONDARY_BUTTON = '[data-test-id^="property-info-secondary-button-"]'
