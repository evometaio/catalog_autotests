class MapLocators:
    """Локаторы для страницы карты."""
    
    # Основной контейнер карты
    MAP_CONTAINER = '[data-testid="map"]'
    
    # Универсальные локаторы для проектов (работают на всех окружениях)
    PROJECT_ELIRE = 'div[aria-label*="Elire"], div[aria-label*="ELIRE"]'
    PROJECT_ARISHA = 'div[aria-label*="Arisha"], div[aria-label*="ARISHA"]'
    PROJECT_CUBIX = 'div[aria-label*="Cubix"], div[aria-label*="CUBIX"]'
    
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
    PROJECT_CARD = 'div.ant-card'
    
    # Универсальные селекторы для всех проектов (работают на всех окружениях)
    ALL_PROJECTS = 'div[aria-label*="Elire"], div[aria-label*="ELIRE"], div[aria-label*="Arisha"], div[aria-label*="ARISHA"], div[aria-label*="Cubix"], div[aria-label*="CUBIX"]'
    ALL_BUTTONS = 'button[aria-label]'
    
    # Навигация на странице проекта
    DUBAI_BUTTON = 'span.ant-menu-title-content'
    PROJECT_PAGE_TITLE = 'h1, h2, h3'
    PROJECT_NAVIGATION = '[class*="CompactNavigation"]'

