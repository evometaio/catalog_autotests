"""Локаторы для проекта Edgewater (MSG)."""

from ..base_locators import BaseLocators


class EdgewaterLocators(BaseLocators):
    """Локаторы для проекта Edgewater."""

    # Основная информация о проекте
    PROJECT_NAME = "edgewater"
    PROJECT_DISPLAY_NAME = "Edgewater"
    # На карте есть 3 проекта: Edgewater Residences 1, 2, 3
    MAP_LOCATOR = 'div[aria-label*="Edgewater Residences"]'

    # Каталог квартир
    PROPERTY_INFO_PRIMARY_BUTTON = '[data-test-id^="property-info-primary-button-"]'
    PROPERTY_INFO_SECONDARY_BUTTON = '[data-test-id^="property-info-secondary-button-"]'

    # Payment Plan
    PAYMENT_PLAN_BUTTON = '[data-test-id="project-info-window-payment-plan-button"]'
    PAYMENT_PLAN_MODAL = ".ant-modal-wrap.ant-modal-centered, [role='dialog']"
    PAYMENT_PLAN_TABLE = ".ant-table-wrapper"
    PAYMENT_PLAN_MODAL_CLOSE = ".ant-modal-close, button:has([aria-label='close'])"

    # Apartment Info Panel (виджет с информацией об аппарте)
    APARTMENT_INFO_PANEL = (
        ".page_propertyCardCard__HXCkB, [class*='propertyInfoWrapper']"
    )
    APARTMENT_INFO_TITLE = "[class*='propertyInfoTitle']"
    APARTMENT_INFO_WRAPPER = "[class*='propertyInfoWrapper']"

    # Pagination
    PAGINATION_ITEM = "li.ant-pagination-item"
    PAGINATION_ITEM_BY_NUMBER = (
        'li.ant-pagination-item-{page_number}, li[title="{page_number}"]'
    )
