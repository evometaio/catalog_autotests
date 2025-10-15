"""Локаторы для страницы карты."""


class MapLocators:
    """Локаторы для страницы карты."""

    # Основной контейнер карты
    MAP_CONTAINER = '[data-testid="map"]'
    
    # Custom POI для тестов
    POI_LOCATOR = '//div[@title="TestPoi"]'

    # Универсальный селектор для всех проектов (используется для проверки загрузки карты)
    ALL_PROJECTS_SELECTOR = (
        'div[aria-label="Elire"], '
        'div[aria-label*="ARISHA"], '
        'div[aria-label*="CUBIX"], '
        'div[aria-label*="Peylaa"], '
        'div[aria-label*="Tranquil"]'
    )

    # Информационные окна проектов
    PROJECT_INFO_WINDOW = 'div.ant-card[class*="_projectInfo"]'
    PROJECT_CARD = "div.ant-card"

    # Универсальные селекторы
    ALL_BUTTONS = "button[aria-label]"
    PROJECT_PAGE_TITLE = "h1, h2, h3"
    PROJECT_NAVIGATION = '[class*="CompactNavigation"]'
