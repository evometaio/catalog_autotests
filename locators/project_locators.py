class ProjectLocators:
    """Базовый класс для локаторов страниц проектов."""

    # Общие константы
    PROJECT_URL_PATTERN = "**/project/**"
    PAGE_TYPES = ["catalog2d", "area", "map"]

    # Названия проектов по застройщикам
    QUBE_PROJECTS = ["arisha", "cubix", "elire"]
    CAPSTONE_PROJECTS = ["peylaa"]
    WELLCUBE_PROJECTS = ["tranquil"]

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


class QubePageLocators(ProjectLocators):
    """Локаторы для страниц проектов Qube (arisha, elire, cubix)."""

    # Агентская страница - для Qube
    class AgentPage:
        """Локаторы для агентских страниц проектов Qube."""

        pass  # Все локаторы перенесены в базовый класс ProjectLocators

    # Клиентская страница -  для Qube
    class ClientPage:
        """Локаторы для клиентских страниц проектов Qube."""

        CALLBACK_FORM_BUTTON = "//button[.//*[@aria-label='phone']]"
        CALLBACK_FORM_MODAL = "//div[@class='ant-modal-content']"

    # Проекты Qube
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

    class Cubix:
        """Локаторы для проекта Cubix."""

        MAP_LOCATOR = 'div[aria-label*="CUBIX RESIDENCE"], div[aria-label*="Cubix"], div[aria-label*="CUBIX"]'
        PROJECT_NAME = "cubix"
        PROJECT_DISPLAY_NAME = "Cubix"

    # Список всех проектов Qube
    ALL_PROJECTS = [Arisha, Elire, Cubix]


class CapstonePageLocators(ProjectLocators):
    """Локаторы для страниц проектов Capstone."""

    # Проекты Capstone
    class Peylaa:
        """Локаторы для проекта Peylaa."""

        MAP_LOCATOR_DEV = 'img[src*="map_pin_peylaa.png"]'
        MAP_LOCATOR_PROD = 'div[aria-label*="Peylaa"]'
        PROJECT_NAME = "peylaa"
        PROJECT_DISPLAY_NAME = "Peylaa"

    # Список всех проектов Capstone
    ALL_PROJECTS = [Peylaa]


class WellcubePageLocators(ProjectLocators):
    """Локаторы для страниц проектов Wellcube."""

    # Проекты Wellcube
    class Tranquil:
        """Локаторы для проекта Tranquil."""

        MAP_LOCATOR = 'div[aria-label*="Tranquil"], div[aria-label*="TRANQUIL"]'
        PROJECT_NAME = "tranquil"
        PROJECT_DISPLAY_NAME = "Tranquil"

    # Список всех проектов Wellcube
    ALL_PROJECTS = [Tranquil]
