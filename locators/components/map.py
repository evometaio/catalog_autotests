"""
Локаторы для карт.
"""

from ..base import locator_registry


def register_map_locators():
    """Регистрирует все локаторы для карт."""

    # === ОСНОВНЫЕ КАРТЫ ===

    locator_registry.add_locator(
        "MAP_CONTAINER",
        '[data-testid="map"]',
        "Основной контейнер карты",
        component="map",
    )

    locator_registry.add_locator(
        "MAP_PROJECT_INFO_WINDOW",
        'div.ant-card[class*="_projectInfo"]',
        "Информационное окно проекта на карте",
        component="map",
    )

    locator_registry.add_locator(
        "MAP_PROJECT_CARD", "div.ant-card", "Карточка проекта на карте", component="map"
    )

    # === НАВИГАЦИЯ ПО КАРТЕ ===

    locator_registry.add_locator(
        "MAP_NAVIGATION",
        '[class*="CompactNavigation"]',
        "Навигация на карте",
        component="map",
    )

    locator_registry.add_locator(
        "MAP_PROJECT_NAVIGATION",
        ".CompactNavigation_navigationContainer__Y5mfa",
        "Навигация по проектам на карте",
        component="map",
    )


# Регистрируем локаторы при импорте
register_map_locators()


class MapLocators:
    """Удобный доступ к локаторам карт."""

    def get(self, name: str, use_fallback: bool = False) -> str:
        """Получить локатор по имени."""
        return locator_registry.get_locator(name, use_fallback)

    def get_all_locators(self) -> dict:
        """Получить все локаторы карт."""
        return locator_registry.get_component_locators("map")


# Экспортируем объект
map_locators = MapLocators()
