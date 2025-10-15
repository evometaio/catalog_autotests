"""Локаторы для проекта Cubix."""

from ..base_locators import BaseLocators


class CubixLocators(BaseLocators):
    """Локаторы для проекта Cubix."""

    # Основная информация о проекте
    PROJECT_NAME = "cubix"
    PROJECT_DISPLAY_NAME = "Cubix"
    MAP_LOCATOR = 'div[aria-label*="CUBIX RESIDENCE"], div[aria-label*="Cubix"], div[aria-label*="CUBIX"]'
