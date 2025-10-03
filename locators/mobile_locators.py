"""
Мобильные локаторы для тестирования на мобильных устройствах.
Содержит все селекторы, специфичные для мобильных устройств.
"""

# ==================== МОБИЛЬНЫЕ СЕЛЕКТОРЫ ПРОЕКТОВ ====================

MOBILE_PROJECT_SELECTORS = {
    "arisha": 'div[aria-label="ARISHA TERRACES"]',
    "elire": 'div[aria-label="Elire"]',
    "cubix": 'div[aria-label="CUBIX RESIDENCE"]',
}

# ==================== МОБИЛЬНЫЕ ЛОКАТОРЫ КАРТЫ ====================

# Модальные окна для мобильных устройств
MOBILE_PROJECT_INFO_MODAL = 'div.ant-modal[class*="_popup"]'
MOBILE_MODAL_MASK = "div.ant-modal-mask"
MOBILE_MODAL_CONTENT = "div.ant-modal-content"

# ==================== МОБИЛЬНЫЕ ЛОКАТОРЫ КНОПОК ====================

# Основные кнопки навигации
MOBILE_EXPLORE_BUTTON = '//span[text()="Explore Project"]'
MOBILE_CLOSE_BUTTON = 'button[aria-label="Close"], .ant-modal-close'

# Навигация по проекту Arisha
MOBILE_ARISHA_MENU_BUTTON = 'button:has-text("arisha")'
MOBILE_ALL_UNITS_BUTTON = "#catalog_2d"

# PDF функциональность
MOBILE_PDF_BUTTON = 'span[aria-label="file-pdf"]'  # PDF кнопка через иконку

# ==================== МОБИЛЬНЫЕ ЛОКАТОРЫ APARTMENTS ====================

# Селекторы для apartments
MOBILE_APARTMENT_SELECTOR = (
    '//span[contains(text(), "VIEW APARTMENT")]'  # Селектор для apartments
)
MOBILE_APARTMENT_LOCK_ICON = (
    'span[aria-label="lock"]'  # Иконка замка для заблокированных apartments
)

# ==================== МОБИЛЬНЫЕ ЛОКАТОРЫ НАВИГАЦИИ ====================

# Элементы навигации
MOBILE_NAVIGATION_MENU = "div.CompactNavigation_navigationContainer__Y5mfa"
MOBILE_NAVIGATION_LIST = "ul.CompactNavigation_list__7sY9t"
MOBILE_MENU_ITEMS = "li.MenuItems_item__pha1O"

# ==================== МОБИЛЬНЫЕ ЛОКАТОРЫ ПРОВЕРОК ====================

# Элементы для проверки адаптивности
MOBILE_VIEWPORT_CONTAINER = "div.pageWrapper"
MOBILE_TOUCH_ELEMENTS = 'button, a, [role="button"]'
MOBILE_MODAL_DIALOG = 'dialog, [role="dialog"]'

# ==================== МОБИЛЬНЫЕ ЛОКАТОРЫ ФОРМ ====================

# Формы и инпуты на мобильных устройствах
MOBILE_FORM_INPUTS = 'input[type="text"], input[type="email"], textarea'
MOBILE_FORM_BUTTONS = 'button[type="submit"], button[type="button"]'

# ==================== МОБИЛЬНЫЕ ЛОКАТОРЫ КОНТЕНТА ====================

# Контентные элементы
MOBILE_CONTENT_IMAGES = 'img[src*="mobile"], img[class*="mobile"]'
MOBILE_CONTENT_TEXT = 'p, span, div[class*="text"]'
MOBILE_CONTENT_LINKS = "a[href]"

# ==================== МОБИЛЬНЫЕ ЛОКАТОРЫ ОШИБОК ====================

# Элементы для обработки ошибок
MOBILE_ERROR_MESSAGES = 'div[class*="error"], span[class*="error"]'
MOBILE_LOADING_INDICATORS = 'div[class*="loading"], span[class*="spinner"]'

# ==================== МОБИЛЬНЫЕ ЛОКАТОРЫ УВЕДОМЛЕНИЙ ====================

# Уведомления и алерты
MOBILE_NOTIFICATION = 'div[class*="notification"], div[class*="alert"]'
MOBILE_TOAST_MESSAGE = 'div[class*="toast"], div[class*="message"]'

# ==================== МОБИЛЬНЫЕ ЛОКАТОРЫ ЗАГРУЗКИ ====================

# Элементы для ожидания загрузки
MOBILE_LOADING_OVERLAY = 'div[class*="loading"], div[class*="overlay"]'
MOBILE_SPINNER = 'div[class*="spinner"], svg[class*="spinner"]'

# ==================== МОБИЛЬНЫЕ ЛОКАТОРЫ СКРОЛЛИНГА ====================

# Элементы для скроллинга
MOBILE_SCROLLABLE_CONTAINER = 'div[class*="scroll"], div[style*="overflow"]'
MOBILE_SCROLL_INDICATOR = 'div[class*="scrollbar"]'

# ==================== МОБИЛЬНЫЕ ЛОКАТОРЫ НАВИГАЦИИ ПО ЗДАНИЯМ/ЭТАЖАМ ====================

# Горизонтальное меню для зданий и этажей
MOBILE_HORIZONTAL_MENU_ITEM = ".react-horizontal-scrolling-menu--item"
MOBILE_BUILDING_SELECTOR = ".react-horizontal-scrolling-menu--item"
MOBILE_FLOOR_SELECTOR = ".react-horizontal-scrolling-menu--item"

# Кнопки навигации
MOBILE_VIEW_BUTTON = "button._button_svuuj_46"

# Модальное окно "Zoom and drag screen"
MOBILE_MODAL_OK_BUTTON = 'button:has-text("OK")'

# ==================== МОБИЛЬНЫЕ ЛОКАТОРЫ КВАРТИР НА ПЛАНЕ ====================

# SVG элементы для квартир
MOBILE_APARTMENT_SVG = "svg"
MOBILE_APARTMENT_PATH = "svg path"
MOBILE_APARTMENT_VISIBLE_CLASS = "_building_1lxa9_1 _animation_1lxa9_7"

# Дополнительные селекторы для квартир
MOBILE_APARTMENT_RECT = "svg rect"
MOBILE_APARTMENT_CIRCLE = "svg circle"

# ==================== ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ====================


def get_mobile_project_selector(project_name: str) -> str:
    """Получить мобильный селектор для проекта по имени."""
    return MOBILE_PROJECT_SELECTORS.get(project_name.lower())


def get_mobile_apartment_selector(apartment_type: str = "VIEW APARTMENT") -> str:
    """Получить селектор для apartment по типу."""
    return f'//span[contains(text(), "{apartment_type}")]'


def get_mobile_button_selector(button_text: str) -> str:
    """Получить селектор для кнопки по тексту."""
    return f'button:has-text("{button_text}")'


def get_mobile_icon_selector(icon_aria_label: str) -> str:
    """Получить селектор для иконки по aria-label."""
    return f'span[aria-label="{icon_aria_label}"]'


def get_mobile_building_selector(building_number: str) -> str:
    """Получить селектор для здания по номеру."""
    return f'{MOBILE_HORIZONTAL_MENU_ITEM}:has-text("{building_number}")'


def get_mobile_floor_selector(floor_number: str) -> str:
    """Получить селектор для этажа по номеру."""
    return f'{MOBILE_HORIZONTAL_MENU_ITEM}:has-text("{floor_number}")'


# ==================== КОНСТАНТЫ ДЛЯ МОБИЛЬНЫХ УСТРОЙСТВ ====================

# Размеры экранов
MOBILE_VIEWPORT_SIZES = {
    "iphone_13": {"width": 390, "height": 844},
    "pixel_5": {"width": 393, "height": 851},
}

# User Agents для мобильных устройств
MOBILE_USER_AGENTS = {
    "iphone_13": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
    "pixel_5": "Mozilla/5.0 (Linux; Android 11; Pixel 5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36",
}

# Таймауты для мобильных устройств (в миллисекундах)
MOBILE_TIMEOUTS = {
    "short": 2000,  # Короткий таймаут для быстрых операций
    "medium": 5000,  # Средний таймаут для обычных операций
    "long": 10000,  # Длинный таймаут для загрузки контента
    "apartment_load": 3500,  # Специальный таймаут для загрузки apartments
}
