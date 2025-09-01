class ProjectLocators:
    """Базовый класс для локаторов страниц проектов."""

    # Общие локаторы для всех проектов
    ALL_UNITS_BUTTON = "//button[.//span[text()='All units']]"
    AVIALABLE_APART_CARD = "(//h3[contains(text(), 'APT. 104')])[2]"
    AVIALABLE_APART = (
        "//span[@class='ant-menu-title-content' and text()='APARTMENT 104']"
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

        MAP_LOCATOR = 'div[aria-label*="Arisha"], div[aria-label*="ARISHA"]'
        PROJECT_NAME = "arisha"
        PROJECT_DISPLAY_NAME = "Arisha"

    class Elire:
        """Локаторы для проекта Elire."""

        MAP_LOCATOR = 'div[aria-label*="Elire"], div[aria-label*="ELIRE"]'
        PROJECT_NAME = "elire"
        PROJECT_DISPLAY_NAME = "Elire"

    class Cubix:
        """Локаторы для проекта Cubix."""

        MAP_LOCATOR = 'div[aria-label*="Cubix"], div[aria-label*="CUBIX"]'
        PROJECT_NAME = "cubix"
        PROJECT_DISPLAY_NAME = "Cubix"

    # Список всех проектов Qube
    ALL_PROJECTS = [Arisha, Elire, Cubix]


class CapstonePageLocators(ProjectLocators):
    """Локаторы для страниц проектов Capstone."""

    # Проекты Capstone
    class Peylaa:
        """Локаторы для проекта Peylaa."""

        MAP_LOCATOR = 'div[aria-label*="Peylaa"], div[aria-label*="PEYLAA"]'
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
