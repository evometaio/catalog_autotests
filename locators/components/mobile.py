"""
Локаторы для мобильных устройств.
"""

from ..base import locator_registry


def register_mobile_locators():
    """Регистрирует все мобильные локаторы."""

    # === МОБИЛЬНЫЕ ЭЛЕМЕНТЫ ===

    locator_registry.add_locator(
        "MOBILE_MAP_CONTAINER",
        '[data-testid="map"]',
        "Контейнер карты для мобильных устройств",
        component="mobile",
    )

    locator_registry.add_locator(
        "MOBILE_INTERFACE",
        '[class*="_mobile_h8wc6_71"]',
        "Мобильный интерфейс",
        component="mobile",
    )

    locator_registry.add_locator(
        "MOBILE_NAVIGATION",
        '[class*="_showOnMobiles_1xz7w_17"]',
        "Мобильная навигация",
        component="mobile",
    )

    # === МОБИЛЬНЫЕ КНОПКИ ===

    locator_registry.add_locator(
        "MOBILE_ALL_BUTTONS",
        "button[aria-label]",
        "Все кнопки с aria-label на мобильных",
        component="mobile",
    )

    locator_registry.add_locator(
        "MOBILE_TOUCH_TARGETS",
        'button, [role="button"], [data-testid*="button"]',
        "Элементы для тач-интерфейса",
        component="mobile",
    )

    # === МОБИЛЬНАЯ НАВИГАЦИЯ ===

    locator_registry.add_locator(
        "MOBILE_PROJECT_NAVIGATION",
        ".CompactNavigation_navigationContainer__Y5mfa",
        "Навигация по проектам на мобильных",
        component="mobile",
    )

    locator_registry.add_locator(
        "MOBILE_BUILDING_NAVIGATION",
        '[class*="_mobile_h8wc6_71"] [data-test-id*="building"]',
        "Навигация по зданиям на мобильных",
        component="mobile",
    )

    locator_registry.add_locator(
        "MOBILE_FLOOR_NAVIGATION",
        '[class*="_mobile_h8wc6_71"] [data-test-id*="floor"]',
        "Навигация по этажам на мобильных",
        component="mobile",
    )

    # === МОБИЛЬНЫЕ ПРОЕКТЫ ===

    locator_registry.add_locator(
        "MOBILE_ARISHA_POINT",
        '[data-test-id="map-project-point-button-mobile-arisha"]',
        "Точка проекта Arisha на мобильной карте",
        component="mobile",
    )

    locator_registry.add_locator(
        "MOBILE_ELIRE_POINT",
        '[data-test-id="map-project-point-button-mobile-elire"]',
        "Точка проекта Elire на мобильной карте",
        component="mobile",
    )

    locator_registry.add_locator(
        "MOBILE_CUBIX_POINT",
        '[data-test-id="map-project-point-button-mobile-cubix"]',
        "Точка проекта Cubix на мобильной карте",
        component="mobile",
    )


# Регистрируем локаторы при импорте
register_mobile_locators()


class MobileLocators:
    """Удобный доступ к мобильным локаторам."""

    def get(self, name: str, use_fallback: bool = False) -> str:
        """Получить локатор по имени."""
        return locator_registry.get_locator(name, use_fallback)

    def get_all_locators(self) -> dict:
        """Получить все мобильные локаторы."""
        return locator_registry.get_component_locators("mobile")

    def get_navigation_locators(self) -> dict:
        """Получить локаторы мобильной навигации."""
        nav_locators = self.get_all_locators()
        return {k: v for k, v in nav_locators.items() if "NAVIGATION" in k}

    def get_project_locators(self) -> dict:
        """Получить локаторы мобильных проектов."""
        project_locators = self.get_all_locators()
        return {k: v for k, v in project_locators.items() if "POINT" in k}


# Экспортируем объект
mobile_locators = MobileLocators()
