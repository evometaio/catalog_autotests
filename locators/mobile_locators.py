"""
Мобильные локаторы для тестирования на мобильных устройствах.

Эти локаторы созданы на основе дебага мобильного интерфейса
и учитывают различия между desktop и mobile версиями.
"""


class MobileLocators:
    """Базовые мобильные локаторы."""

    # Основные мобильные элементы
    MOBILE_MAP_CONTAINER = '[data-testid="map"]'
    MOBILE_INTERFACE = '[class*="_mobile_h8wc6_71"]'
    MOBILE_NAVIGATION = '[class*="_showOnMobiles_1xz7w_17"]'
    
    # Мобильные кнопки и элементы управления
    MOBILE_ALL_BUTTONS = "button[aria-label]"
    MOBILE_TOUCH_TARGETS = 'button, [role="button"], [data-testid*="button"]'
    
    # Мобильная навигация
    MOBILE_PROJECT_NAVIGATION = '.CompactNavigation_navigationContainer__Y5mfa'
    MOBILE_PROJECT_ITEMS = '[class*="CompactNavigation"] button'
    
    # Мобильные проекты (те же локаторы, что и на desktop, но проверяем видимость)
    MOBILE_ARISHA_PROJECT = 'div[aria-label*="ARISHA TERACCES"], div[aria-label*="Arisha"], div[aria-label*="ARISHA"]'
    MOBILE_ELIRE_PROJECT = 'div[aria-label*="ELIRE"], div[aria-label*="Elire"]'
    MOBILE_CUBIX_PROJECT = 'div[aria-label*="CUBIX RESIDENCE"], div[aria-label*="Cubix"], div[aria-label*="CUBIX"]'
    
    # Мобильные кнопки (найденные через дебаг)
    MOBILE_EXPLORE_PROJECT_ARISHA = '[data-test-id="map-project-point-button-mobile-arisha"]'
    MOBILE_EXPLORE_PROJECT_ELIRE = '[data-test-id="map-project-point-button-mobile-elire"]'
    MOBILE_EXPLORE_PROJECT_CUBIX = '[data-test-id="map-project-point-button-mobile-cubix"]'
    MOBILE_MENU_TOGGLE = '[data-test-id="nav-mobile-menu-toggle"]'
    MOBILE_CONTACT_BUTTON = '[data-test-id="contact-button"]'
    MOBILE_BACK_BUTTON = '[data-test-id="nav-button-back"]'
    
    # Мобильные информационные элементы
    MOBILE_PROJECT_INFO = '[class*="_showOnMobiles_"]'
    MOBILE_PROJECT_CARD = '[class*="_showOnMobiles_"] .ant-card'
    MOBILE_MODAL_CONTENT = '.ant-modal-content'
    
    # Элементы, которые скрыты на мобильных
    DESKTOP_ONLY_ELEMENTS = '[class*="_showOnDesktops_"], [class*="desktop-only"]'
    
    # Мобильные специфичные элементы
    MOBILE_BROCHURE_BUTTON = 'button:has-text("Get brochure")'
    MOBILE_PROJECT_TITLE = '[class*="_showOnMobiles_"] h1, [class*="_showOnMobiles_"] h2, [class*="_showOnMobiles_"] h3'
    
    # Мобильная навигация по зданиям и этажам (найденные через дебаг)
    MOBILE_CHOOSE_BUILDING_BUTTON = 'button:has-text("Choose the building")'
    MOBILE_BUILDING_SVG_ELEMENTS = 'svg path[class*="_building_"]'
    MOBILE_ACTIVE_BUILDING = 'svg path[class*="_animationActive_"]'
    
    # Мобильная навигация (компактная)
    MOBILE_COMPACT_NAVIGATION = '.CompactNavigation_navigationContainer__Y5mfa._showOnMobiles_1xz7w_17'
    MOBILE_NAV_MENU = '.CompactNavigation_menu__jJlV0'
    
    # Мобильные апартаменты на плане этажа
    MOBILE_FLOOR_PLAN_APARTMENTS = '[class*="_showOnMobiles_"] svg [class*="apartment"]'
    
    # Мобильные кнопки управления
    MOBILE_ROTATION_CONTROLS = '[data-test-id="nav-rotation-view-controls-button"]'


class MobileQubeLocators(MobileLocators):
    """Мобильные локаторы для проектов Qube."""
    
    # Qube специфичные мобильные элементы
    MOBILE_QUBE_PROJECTS = [
        MOBILE_ARISHA_PROJECT,
        MOBILE_ELIRE_PROJECT, 
        MOBILE_CUBIX_PROJECT
    ]
    
    # Мобильные элементы для Arisha
    MOBILE_ARISHA_WIDGET = '[class*="_showOnMobiles_"] [class*="apartment-widget"]'
    MOBILE_ARISHA_VIEW_2D = '[class*="_showOnMobiles_"] button:has-text("2D")'
    MOBILE_ARISHA_VIEW_3D = '[class*="_showOnMobiles_"] button:has-text("3D")'
    
    # Мобильные элементы для Elire
    MOBILE_ELIRE_RESIDENCES_BUTTON = '[class*="_showOnMobiles_"] button:has-text("Residences")'
    MOBILE_ELIRE_REQUEST_VIEWING = '[class*="_showOnMobiles_"] button:has-text("Request Viewing")'
    
    # Мобильные элементы для Cubix
    MOBILE_CUBIX_SALES_OFFER = '[class*="_showOnMobiles_"] button:has-text("Sales Offer")'


class MobileCapstoneLocators(MobileLocators):
    """Мобильные локаторы для проектов Capstone."""
    
    # Capstone специфичные мобильные элементы
    MOBILE_PEYLAA_PROJECT = 'div[aria-label*="Peylaa"], div[aria-label*="PEYLAA"]'
    MOBILE_CAPSTONE_EXPLORE = '[class*="_showOnMobiles_"] button:has-text("Explore")'


class MobileWellcubeLocators(MobileLocators):
    """Мобильные локаторы для проектов Wellcube."""
    
    # Wellcube специфичные мобильные элементы
    MOBILE_TRANQUIL_PROJECT = 'div[aria-label*="Tranquil"], div[aria-label*="TRANQUIL"]'
    MOBILE_WELLCUBE_DOWNLOAD = '[class*="_showOnMobiles_"] button:has-text("Download")'
    MOBILE_WELLCUBE_OWNERSHIP = '[class*="_showOnMobiles_"] button:has-text("ownership")'


# Утилитарные функции для работы с мобильными локаторами
class MobileLocatorUtils:
    """Утилиты для работы с мобильными локаторами."""
    
    @staticmethod
    def get_mobile_project_locator(project_name: str) -> str:
        """Получить мобильный локатор для конкретного проекта."""
        project_locators = {
            "arisha": MobileQubeLocators.MOBILE_ARISHA_PROJECT,
            "elire": MobileQubeLocators.MOBILE_ELIRE_PROJECT,
            "cubix": MobileQubeLocators.MOBILE_CUBIX_PROJECT,
            "peylaa": MobileCapstoneLocators.MOBILE_PEYLAA_PROJECT,
            "tranquil": MobileWellcubeLocators.MOBILE_TRANQUIL_PROJECT,
        }
        return project_locators.get(project_name.lower(), "")
    
    @staticmethod
    def get_mobile_navigation_locators() -> list:
        """Получить список всех мобильных навигационных локаторов."""
        return [
            MobileLocators.MOBILE_BUILDING_NAV,
            MobileLocators.MOBILE_FLOOR_NAV,
            MobileLocators.MOBILE_APARTMENT_NAV,
        ]
    
    @staticmethod
    def get_mobile_only_elements() -> list:
        """Получить список локаторов только для мобильных устройств."""
        return [
            MobileLocators.MOBILE_INTERFACE,
            MobileLocators.MOBILE_NAVIGATION,
            MobileLocators.MOBILE_PROJECT_INFO,
        ]
    
    @staticmethod
    def get_desktop_only_elements() -> list:
        """Получить список локаторов только для desktop."""
        return [
            MobileLocators.DESKTOP_ONLY_ELEMENTS,
        ]
