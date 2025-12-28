"""Локаторы для проекта Willows Residences (Abra)."""

from ..base_locators import BaseLocators


class WillowsResidencesLocators(BaseLocators):
    """Локаторы для проекта Willows Residences."""

    # Основная информация о проекте
    PROJECT_NAME = "willows_residences"
    PROJECT_DISPLAY_NAME = "Willows Residences"
    MAP_LOCATOR = 'div[aria-label*="Willows"], div[aria-label*="WILLOWS"], div[aria-label*="Willows Residences"]'

    # Каталог квартир
    PROPERTY_INFO_PRIMARY_BUTTON = '[data-test-id^="property-info-primary-button-"]'
    PROPERTY_INFO_SECONDARY_BUTTON = '[data-test-id^="property-info-secondary-button-"]'

    # View Brochures
    VIEW_BROCHURES_BUTTON = '[data-test-id="project-info-window-secondary-button"]'

    # Apartment Info Panel (виджет с информацией об аппарте)
    APARTMENT_INFO_PANEL = (
        ".page_propertyCardCard__HXCkB, .page_propertyInfoWrapper__br3pL"
    )
    APARTMENT_INFO_TITLE = (
        '[class*="propertyInfoTitle"], .page_propertyInfoTitleWrapper__asvoO'
    )
    APARTMENT_INFO_WRAPPER = ".page_propertyInfoWrapper__br3pL"

    # Pagination
    PAGINATION_ITEM = "li.ant-pagination-item"
    PAGINATION_ITEM_BY_NUMBER = (
        'li.ant-pagination-item-{page_number}, li[title="{page_number}"]'
    )
