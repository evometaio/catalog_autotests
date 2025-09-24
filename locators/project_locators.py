class BaseProjectLocators:
    """Базовый класс для всех локаторов проектов."""

    # Общие константы
    PROJECT_URL_PATTERN = "**/project/**"
    PAGE_TYPES = ["catalog2d", "area", "map"]

    # Общие локаторы для всех проектов
    ALL_UNITS_BUTTON = '[data-test-id="nav-desktop-catalog2d-standalone"]'

    # Универсальные локаторы для поиска апартаментов
    ALL_APARTMENT_TITLES = "//span[contains(text(), 'VIEW APARTMENT')]"
    DUBAI_BUTTON = '(//span[text()="Dubai"])[1]'
    DUBAI_BUTTON_CUB = '(//span[text()="Dubai"])'

    # Базовые локаторы для Explore Amenities (могут быть переопределены в подклассах)
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
    AREA_TOUR_360_MODAL = "//div[contains(@class, 'modal')]"
    AREA_TOUR_360_OVERLAY = "//div[contains(@class, 'overlay')]"
    AREA_TOUR_360_CLOSE_BUTTON = (
        "//button[contains(@class, 'close') and @aria-label='close']"
    )
    AREA_TOUR_360_CONTENT = (
        "//img[contains(@class, '__react-image-turntable-img')] | //video | //canvas"
    )

    # Агентские функции - доступны на агентских страницах
    SALES_OFFER_BUTTON = "//span[text()='Sales Offer']"
    DOWNLOAD_PDF_BUTTON = "//button[.//span[text() = 'Download PDF']]"

    # Навигация по зданиям и этажам - доступны на всех страницах проектов
    BUILDING_NAV_BUTTON = '[data-test-id="nav-desktop-building"]'
    FLOOR_NAV_BUTTON = '[data-test-id="nav-desktop-floor"]'
    APARTMENT_NAV_BUTTON = '[data-test-id="nav-desktop-apartment"]'

    # Селекторы для конкретных зданий и этажей
    BUILDING_1_BUTTON = '[data-test-id="nav-desktop-building-1"]'
    BUILDING_2_BUTTON = '[data-test-id="nav-desktop-building-2"]'
    BUILDING_3_BUTTON = '[data-test-id="nav-desktop-building-3"]'

    FLOOR_1_BUTTON = '[data-test-id="nav-desktop-floor-1"]'
    FLOOR_2_BUTTON = '[data-test-id="nav-desktop-floor-2"]'
    FLOOR_3_BUTTON = '[data-test-id="nav-desktop-floor-3"]'
    FLOOR_4_BUTTON = '[data-test-id="nav-desktop-floor-4"]'
    FLOOR_5_BUTTON = '[data-test-id="nav-desktop-floor-5"]'
    FLOOR_6_BUTTON = '[data-test-id="nav-desktop-floor-6"]'
    FLOOR_7_BUTTON = '[data-test-id="nav-desktop-floor-7"]'

    # Селектор для апартаментов на плане этажа
    FLOOR_PLAN_APARTMENTS = 'svg [class*="apartment"]'


class QubeLocators(BaseProjectLocators):
    """Локаторы для проектов Qube (Arisha, Elire, Cubix)."""

    # Названия проектов Qube
    QUBE_PROJECTS = ["arisha", "cubix", "elire"]
    ALL_PROJECTS = []

    class Arisha:
        """Локаторы для проекта Arisha."""

        MAP_LOCATOR = 'div[aria-label*="ARISHA TERACCES"], div[aria-label*="Arisha"], div[aria-label*="ARISHA"]'
        PROJECT_NAME = "arisha"
        PROJECT_DISPLAY_NAME = "Arisha"

    class Elire:
        """Локаторы для проекта Elire."""

        MAP_LOCATOR = 'div[aria-label="Elire"]'
        PROJECT_NAME = "elire"
        PROJECT_DISPLAY_NAME = "Elire"
        RESIDENCES_BUTTON = '[data-test-id="nav-desktop-catalog2d"]'
        REQUEST_VIEWING_BUTTON = "(//button[@data-test-id='property-info-secondary-button-1 BEDROOM RESIDENCE'])[2]"
        START_3D_EXPANSION_BUTTON = "//button[contains(text(), 'Start 3D Experience')]"
        SUBMIT_BUTTON_FOR_REQUEST_VIEWING = "(//button[.//span[text()='SUBMIT']])[2]"

        # Локаторы для полей формы Request Viewing
        FIRST_NAME_FIELD = "(//input[@id='first_name'])[2]"
        LAST_NAME_FIELD = "(//input[@id='last_name'])[2]"
        PHONE_FIELD = "(//input[@id='phone'])[2]"
        EMAIL_FIELD = "(//input[@id='email'])[2]"
        NOTE_FIELD = "(//textarea[@id='note'])[2]"

        # Локаторы для модального окна успешной отправки
        SUCCESS_MODAL = 'xpath=(//div[@class="ant-modal-content"])[1]'
        SUCCESS_MODAL_TITLE = 'xpath=.//div[contains(text(), "Thank you!")]'
        SUCCESS_MODAL_TEXT = (
            'xpath=.//div[contains(text(), "Our specialist will contact you shortly.")]'
        )

        # Специфичные локаторы для Explore Amenities в Elire
        EXPLORE_AMENITIES_BUTTON = (
            '(//button[@data-test-id="project-info-window-explore-amenities"])[2]'
        )
        AMENITIES_MODAL = ".ant-modal-content"
        AMENITIES_MODAL_TITLE = ".ant-modal-content h3._title_6w0b9_41"
        AMENITIES_MODAL_CLOSE_BUTTON = ".ant-modal-close"

        # Локатор для Start 3D Experience 1 Bedroom Residence
        START3DEXPREINCE_1BEDROOM_RESIDENCE = '(//button[@data-test-id="property-info-primary-button-1 BEDROOM RESIDENCE"])[2]'

    class Cubix:
        """Локаторы для проекта Cubix."""

        MAP_LOCATOR = 'div[aria-label*="CUBIX RESIDENCE"], div[aria-label*="Cubix"], div[aria-label*="CUBIX"]'
        PROJECT_NAME = "cubix"
        PROJECT_DISPLAY_NAME = "Cubix"

    # Локаторы для клиентских страниц Qube проектов
    CALLBACK_FORM_BUTTON = "//button[.//*[@aria-label='phone']]"
    CALLBACK_FORM_MODAL = "//div[@class='ant-modal-content']"

    def __init__(self):
        """Инициализация списка всех проектов Qube."""
        self.ALL_PROJECTS = [self.Arisha, self.Elire, self.Cubix]


class WellcubePageLocators(BaseProjectLocators):
    """Локаторы для проектов Wellcube."""

    # Названия проектов Wellcube
    WELLCUBE_PROJECTS = ["tranquil"]
    ALL_PROJECTS = []

    class Tranquil:
        """Локаторы для проекта Tranquil."""

        MAP_LOCATOR = 'div[aria-label*="Tranquil"], div[aria-label*="TRANQUIL"]'
        PROJECT_NAME = "tranquil"
        PROJECT_DISPLAY_NAME = "Tranquil"
        FRACTION_OWNERSHIP_OFFER_BUTTON = (
            '(//button[@data-test-id="property-info-primary-button-1102 A"])[2]'
        )

    def __init__(self):
        """Инициализация списка всех проектов Wellcube."""
        self.ALL_PROJECTS = [self.Tranquil]


class CapstonePageLocators(BaseProjectLocators):
    """Локаторы для проектов Capstone."""

    # Названия проектов Capstone
    CAPSTONE_PROJECTS = ["peylaa"]
    ALL_PROJECTS = []

    class Peylaa:
        """Локаторы для проекта Peylaa."""

        MAP_LOCATOR_DEV = 'img[src*="map_pin_peylaa.png"]'
        MAP_LOCATOR_PROD = 'div[aria-label*="Peylaa"]'
        PROJECT_NAME = "peylaa"
        PROJECT_DISPLAY_NAME = "Peylaa"

    def __init__(self):
        """Инициализация списка всех проектов Capstone."""
        self.ALL_PROJECTS = [self.Peylaa]
