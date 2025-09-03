from .project_locators import QubePageLocators


class MapLocators:
    """Локаторы для страницы карты."""

    # Основной контейнер карты
    MAP_CONTAINER = '[data-testid="map"]'

    # Локаторы для проектов Qube через новый класс
    PROJECT_ELIRE = QubePageLocators.Elire.MAP_LOCATOR
    PROJECT_ARISHA = QubePageLocators.Arisha.MAP_LOCATOR
    PROJECT_CUBIX = QubePageLocators.Cubix.MAP_LOCATOR

    # Универсальный селектор для всех проектов Qube
    ALL_PROJECTS = f"{PROJECT_ELIRE}, {PROJECT_ARISHA}, {PROJECT_CUBIX}"
    
    # Универсальный селектор для всех проектов (включая Capstone и Wellcube)
    ALL_PROJECTS_SELECTOR = 'div[aria-label*="Elire"], div[aria-label*="ELIRE"], div[aria-label*="ARISHA TERACCES"], div[aria-label*="Arisha"], div[aria-label*="ARISHA"], div[aria-label*="CUBIX RESIDENCE"], div[aria-label*="Cubix"], div[aria-label*="CUBIX"], li:has-text("peylaa"), span:has-text("Peylaa"), div[aria-label*="Peylaa"], div[aria-label*="PEYLAA"], li:has-text("tranquil"), span:has-text("Tranquil"), div[aria-label*="Tranquil"], div[aria-label*="TRANQUIL"]'

    # Элементы управления картой (основные)
    ZOOM_IN_BUTTON = '[aria-label="Увеличить"]'
    ZOOM_OUT_BUTTON = '[aria-label="Уменьшить"]'
    FULLSCREEN_BUTTON = '[aria-label="Включить полноэкранный режим"]'

    # Альтернативные локаторы для элементов управления
    ZOOM_IN_ALT = 'button[title="Увеличить"], button[aria-label*="zoom"], button[aria-label*="Zoom"]'
    ZOOM_OUT_ALT = 'button[title="Уменьшить"], button[aria-label*="zoom"], button[aria-label*="Zoom"]'
    FULLSCREEN_ALT = 'button[title*="полноэкран"], button[aria-label*="fullscreen"], button[aria-label*="Fullscreen"]'

    # Информационные окна проектов
    PROJECT_INFO_WINDOW = 'div.ant-card[class*="_projectInfo"]'
    PROJECT_CARD = "div.ant-card"

    # Универсальные селекторы для всех проектов (работают на всех окружениях)
    ALL_BUTTONS = "button[aria-label]"

    # Навигация на странице проекта
    DUBAI_BUTTON = "span.ant-menu-title-content"
    PROJECT_PAGE_TITLE = "h1, h2, h3"
    PROJECT_NAVIGATION = '[class*="CompactNavigation"]'
    EXPLORE_PROJECT_BUTTON = "//span[text()='Explore Project']"
