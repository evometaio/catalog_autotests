class ProjectLocators:
    """Базовый класс для локаторов страниц проектов."""

    # Общие локаторы для всех проектов
    ALL_UNITS_BUTTON = "//div[contains(@style, 'All units')]//button"

    # Универсальные локаторы для поиска апартаментов
    ALL_APARTMENT_TITLES = (
        "//span[contains(text(), 'VIEW APARTMENT')]"
    )


class QubePageLocators(ProjectLocators):
    """Локаторы для страниц проектов Qube (arisha, elire, cubix)."""

    # Агентская страница - специфичные для Qube
    class AgentPage:
        """Локаторы для агентских страниц проектов Qube."""

        SALES_OFFER_BUTTON = "//button[.//span[text() = 'Sales Offer']]"
        DOWNLOAD_PDF_BUTTON = "//button[.//span[text() = 'Download PDF']]"

    # Клиентская страница - специфичные для Qube
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

        MAP_LOCATOR = 'div[aria-label*="Elire"], div[aria-label*="ELIRE"]'
        PROJECT_NAME = "elire"
        PROJECT_DISPLAY_NAME = "Elire"
        RESIDENCES_BUTTON = (
            "//li[@role='menuitem' and .//span[text()='Residences']]"
        )
        REQUEST_VIEWING_BUTTON = "(//button[.//span[text()='REQUEST VIEWING']])[6]"
        SUBMIT_BUTTON_FOR_REQUEST_VIEWING = "(//button[.//span[text()='SUBMIT']])[1]"

        # Локаторы для полей формы Request Viewing (используем [2] - вторые поля)
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

        MAP_LOCATOR = 'li:has-text("peylaa"), span:has-text("Peylaa"), div[aria-label*="Peylaa"], div[aria-label*="PEYLAA"]'
        PROJECT_NAME = "peylaa"
        PROJECT_DISPLAY_NAME = "Peylaa"

    # Список всех проектов Capstone
    ALL_PROJECTS = [Peylaa]


class WellcubePageLocators(ProjectLocators):
    """Локаторы для страниц проектов Wellcube."""

    # Проекты Wellcube
    class Tranquil:
        """Локаторы для проекта Tranquil."""

        MAP_LOCATOR = 'li:has-text("tranquil"), span:has-text("Tranquil"), div[aria-label*="Tranquil"], div[aria-label*="TRANQUIL"]'
        PROJECT_NAME = "tranquil"
        PROJECT_DISPLAY_NAME = "Tranquil"

    # Список всех проектов Wellcube
    ALL_PROJECTS = [Tranquil]
