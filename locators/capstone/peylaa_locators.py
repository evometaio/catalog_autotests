"""Локаторы для проекта Peylaa (Capstone)."""

from ..base_locators import BaseLocators


class PeylaaLocators(BaseLocators):
    """Локаторы для проекта Peylaa."""

    # Основная информация о проекте
    PROJECT_NAME = "peylaa"
    PROJECT_DISPLAY_NAME = "Peylaa"

    # MAP локаторы для разных окружений
    MAP_LOCATOR_DEV = 'div[title="Peylaa"][aria-label="Peylaa"]'
    MAP_LOCATOR_PROD = 'div[aria-label*="Peylaa"]'
