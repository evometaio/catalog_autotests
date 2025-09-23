from .project_locators import QubeLocators


class MapLocators:
    """Локаторы для страницы карты."""

    # Основной контейнер карты
    MAP_CONTAINER = '[data-testid="map"]'

    # Локаторы для проектов Qube через новый класс
    PROJECT_ELIRE = QubeLocators.Elire.MAP_LOCATOR
    PROJECT_ARISHA = QubeLocators.Arisha.MAP_LOCATOR
    PROJECT_CUBIX = QubeLocators.Cubix.MAP_LOCATOR

    # Универсальный селектор для всех проектов Qube
    ALL_PROJECTS = f"{PROJECT_ELIRE}, {PROJECT_ARISHA}, {PROJECT_CUBIX}"

    # Универсальный селектор для всех проектов
    ALL_PROJECTS_SELECTOR = 'div[aria-label="Elire"], div[aria-label*="ARISHA TERACCES"], div[aria-label*="Arisha"], div[aria-label*="ARISHA"], div[aria-label*="CUBIX RESIDENCE"], div[aria-label*="Cubix"], div[aria-label*="CUBIX"], li:has-text("peylaa"), span:has-text("Peylaa"), div[aria-label*="Peylaa"], div[aria-label*="PEYLAA"], li:has-text("tranquil"), span:has-text("Tranquil"), div[aria-label*="Tranquil"], div[aria-label*="TRANQUIL"]'

    # Информационные окна проектов
    PROJECT_INFO_WINDOW = 'div.ant-card[class*="_projectInfo"]'
    PROJECT_CARD = "div.ant-card"

    # Универсальные селекторы для всех проектов
    ALL_BUTTONS = "button[aria-label]"

    # Навигация на странице проекта
    PROJECT_PAGE_TITLE = "h1, h2, h3"
    PROJECT_NAVIGATION = '[class*="CompactNavigation"]'
    EXPLORE_PROJECT_BUTTON = "//span[text()='Explore Project']"
