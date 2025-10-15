"""Базовые локаторы, общие для всех проектов."""


class BaseLocators:
    """Базовые локаторы для всех проектов."""

    # Общие константы
    PROJECT_URL_PATTERN = "**/project/**"
    PAGE_TYPES = ["catalog_2d", "area", "map"]

    # Общие кнопки навигации
    ALL_UNITS_BUTTON = '[data-test-id="nav-desktop-catalog2d-standalone"]'

    # Универсальные локаторы для поиска апартаментов
    ALL_APARTMENT_TITLES = "//span[contains(text(), 'VIEW APARTMENT')]"

    # Локаторы для Explore Amenities (общие для всех проектов)
    EXPLORE_AMENITIES_BUTTON = (
        '(//button[@data-test-id="project-info-window-explore-amenities"])[2]'
    )
    AMENITIES_MODAL = ".ant-modal-content"
    AMENITIES_MODAL_TITLE = ".ant-modal-content h3"
    AMENITIES_MODAL_CLOSE_BUTTON = ".ant-modal-close"

    # Локаторы для слайдера в модалке amenities
    AMENITIES_SLIDER = ".slick-slider"
    AMENITIES_SLIDER_IMAGES = ".slick-slider img"
    AMENITIES_SLIDER_INDICATORS = ".slick-dots li"
    AMENITIES_SLIDER_PREV_BUTTON = ".slick-prev"
    AMENITIES_SLIDER_NEXT_BUTTON = ".slick-next"

    # 360 Area Tour - доступен на всех страницах проектов
    AREA_TOUR_360_BUTTON = '[data-test-id="nav-rotation-view-controls-button"]'
    AREA_TOUR_360_MODAL = '[data-test-id="rotation-view-360-modal"]'
    AREA_TOUR_360_OVERLAY = '[data-test-id="rotation-view-360-overlay"]'
    AREA_TOUR_360_CLOSE_BUTTON = 'button[data-test-id="rotation-view-360-close-button"]'
    AREA_TOUR_360_CONTENT = (
        "//img[contains(@class, '__react-image-turntable-img')] | //video | //canvas"
    )

    # Агентские функции
    SALES_OFFER_BUTTON = "//span[text()='Sales Offer']"
    DOWNLOAD_PDF_BUTTON = "//button[.//span[text() = 'Download PDF']]"

    # Навигация по зданиям и этажам
    BUILDING_NAV_BUTTON = '[data-test-id="nav-desktop-building"]'
    FLOOR_NAV_BUTTON = '[data-test-id="nav-desktop-floor"]'
    APARTMENT_NAV_BUTTON = '[data-test-id="nav-desktop-apartment"]'

    # Примечание: Селекторы для конкретных зданий/этажей формируются динамически
    # Здание: f'[data-test-id="nav-desktop-building-{number}"]'
    # Этаж: f'[data-test-id="nav-desktop-floor-{number}"]'

    # Селектор для апартаментов на плане этажа
    FLOOR_PLAN_APARTMENTS = 'svg [class*="apartment"]'

    # Локаторы для клиентских страниц
    CALLBACK_FORM_BUTTON = "//button[.//*[@aria-label='phone']]"
    CALLBACK_FORM_MODAL = "//div[@class='ant-modal-content']"
