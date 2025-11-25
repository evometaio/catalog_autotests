"""Локаторы для проекта MARK (LSR)."""

from ..base_locators import BaseLocators


class MarkLocators(BaseLocators):
    """Локаторы для проекта MARK."""

    # Основная информация о проекте
    PROJECT_NAME = "mark"
    PROJECT_DISPLAY_NAME = "MARK"

    # Навигация
    NAV_DESKTOP_CATALOG2D_STANDALONE = (
        '[data-test-id="nav-desktop-catalog2d-standalone"]'
    )
    NAV_DESKTOP_PROJECT_MARK = '[data-test-id="nav-desktop-project-mark"]'
    NAV_DESKTOP_BUILDING = '[data-test-id="nav-desktop-building"]'
    NAV_DESKTOP_VIEW3D_STANDALONE = '[data-test-id="nav-desktop-view3d-standalone"]'

    # Мобильная навигация
    NAV_MOBILE_MENU_TOGGLE = '[data-test-id="nav-mobile-menu-toggle"]'
    NAV_MOBILE_CATALOG2D = '[data-test-id="nav-mobile-catalog2d"]'

    # Кнопки
    CONTACT_BUTTON = '[data-test-id="contact-button"]'
    NAV_BUTTON_BACK = '[data-test-id="nav-button-back"]'

    # 360 Area Tour (используем базовый локатор, но переопределяем если нужно)
    AREA_TOUR_360_BUTTON = '[data-test-id="nav-rotation-view-controls-button"]'

    # Меню выбора панорам (появляется после клика на кнопку Панорамы)
    AREA_TOUR_360_MENU_ROTATION = (
        '[data-test-id="nav-rotation-view-controls-menu-rotation"]'
    )
    AREA_TOUR_360_MENU_TOUR_YARD = (
        '[data-test-id="nav-rotation-view-controls-menu-tour-yard"]'
    )
    AREA_TOUR_360_MENU_TOUR_LOBBY_K1 = (
        '[data-test-id="nav-rotation-view-controls-menu-tour-lobby-k1"]'
    )
    AREA_TOUR_360_MENU_TOUR_LOBBY_K2 = (
        '[data-test-id="nav-rotation-view-controls-menu-tour-lobby-k2"]'
    )
    AREA_TOUR_360_MENU_TOUR_LOBBY_K3 = (
        '[data-test-id="nav-rotation-view-controls-menu-tour-lobby-k3"]'
    )

    # Общий селектор для всех пунктов меню панорам
    AREA_TOUR_360_MENU_ITEMS = '[data-test-id^="nav-rotation-view-controls-menu-"]'

    # Модальное окно 360 тура (для MARK может отличаться)
    # Для rotation типа используется модальное окно, для остальных - iframe
    AREA_TOUR_360_MODAL = (
        '[data-test-id="rotation-view-360-modal"], .ant-modal-content, [role="dialog"]'
    )
    AREA_TOUR_360_CLOSE_BUTTON = 'button[data-test-id="rotation-view-360-close-button"], .ant-modal-close, button[aria-label="close"]'
    # Контент для rotation типа (много изображений)
    AREA_TOUR_360_CONTENT = (
        '[data-test-id="rotation-view-360-content"] img, iframe, canvas, video'
    )

    # Кнопка выбора панорамы в модальном окне
    TOURS3D_MENU_DROPDOWN_BUTTON = '[data-test-id="tours3d-menu-dropdown-button"]'

    # Каталог квартир
    PROPERTY_FILTER_RESET_BUTTON = '[data-test-id="property-filter-reset-button"]'

    # Паттерны для кнопок квартир (динамические)
    PROPERTY_INFO_PRIMARY_BUTTON = '[data-test-id^="property-info-primary-button-"]'
    PROPERTY_INFO_SECONDARY_BUTTON = '[data-test-id^="property-info-secondary-button-"]'

    # Кнопка скачивания PDF (в виджете апартамента - первая кнопка)
    DOWNLOAD_PDF_BUTTON = '[data-test-id="info-content-secondary-button"]'
    # Кнопка скачивания PDF для мобильной версии (второй элемент)
    DOWNLOAD_PDF_BUTTON_MOBILE = (
        '(//button[@data-test-id="info-content-secondary-button"])[2]'
    )
    # Альтернативный локатор через текст
    DOWNLOAD_PDF_BUTTON_TEXT = 'button:has-text("Скачать PDF")'

    # Кнопка дополнительного меню на мобильном (info-circle)
    MOBILE_INFO_MENU_BUTTON = (
        "button._showOnMobiles_158xm_17, button:has(.anticon-info-circle)"
    )

    # Кнопка скачивания PDF в модальном окне (вторая кнопка после загрузки)
    # Используем уникальный класс page_modalSalesOfferButton__Jw6OU для точного поиска
    DOWNLOAD_PDF_MODAL_BUTTON = (
        '//button[contains(@class, "page_modalSalesOfferButton__Jw6OU")]'
    )

    # Модальное окно с PDF
    PDF_MODAL = '.ant-modal-content, [role="dialog"]'

    # Переопределяем базовые локаторы для MARK
    ALL_UNITS_BUTTON = NAV_DESKTOP_CATALOG2D_STANDALONE
    # Для MARK используем кнопки квартир вместо текста "VIEW APARTMENT"
    ALL_APARTMENT_TITLES = '[data-test-id^="property-info-primary-button-"]'

    # Локаторы для виджета апартамента
    class ApartmentWidget:
        """Локаторы для виджета апартамента MARK."""

        # Кнопки режимов просмотра (используют классы, а не текст)
        VIEW_2D_BUTTON = ".widget-control-button.control-2d"
        VIEW_3D_BUTTON = ".widget-control-button.control-3d"

        # Кнопки навигации по сценам (в MARK стрелки появляются только в 3D режиме)
        # Используем второй элемент, так как первый может быть скрыт
        PREV_ARROW = 'xpath=(//button[contains(@class, "arrow-button--reverse")])[2]'
        NEXT_ARROW = 'xpath=(//button[contains(@class, "arrow-button") and not(contains(@class, "arrow-button--reverse"))])[2]'

        # Индикатор сцен (в MARK это текст "1/13" в widget-arrow-controls__text, используем второй элемент)
        SCENE_INDICATOR = (
            'xpath=(//div[contains(@class, "widget-arrow-controls__text")])[2]'
        )

        # Кнопка зума (0.5x)
        SPEED_BUTTON = '.widget-control-button.control-scale, button:has-text("0.5x")'
