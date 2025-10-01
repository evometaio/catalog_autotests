"""
Общие локаторы для всех проектов.
"""

from ..base import locator_registry


def register_common_locators():
    """Регистрирует общие локаторы для всех проектов."""

    # === ОБЩИЕ ЭЛЕМЕНТЫ ===

    locator_registry.add_locator(
        "COMMON_MAP_CONTAINER",
        '[data-testid="map"]',
        "Основной контейнер карты",
        project="common",
        component="map",
    )

    locator_registry.add_locator(
        "COMMON_ALL_PROJECTS",
        'div[aria-label="Elire"], div[aria-label*="ARISHA TERACCES"], div[aria-label*="Arisha"], div[aria-label*="ARISHA"], div[aria-label*="CUBIX RESIDENCE"], div[aria-label*="Cubix"], div[aria-label*="CUBIX"], li:has-text("peylaa"), span:has-text("Peylaa"), div[aria-label*="Peylaa"], div[aria-label*="PEYLAA"], li:has-text("tranquil"), span:has-text("Tranquil"), div[aria-label*="Tranquil"], div[aria-label*="TRANQUIL"]',
        "Универсальный селектор для всех проектов",
        project="common",
        component="map",
    )

    # === МОДАЛЬНЫЕ ОКНА ===

    locator_registry.add_locator(
        "COMMON_MODAL_CONTENT",
        ".ant-modal-content",
        "Контент модального окна",
        project="common",
        component="modal",
    )

    locator_registry.add_locator(
        "COMMON_MODAL_CLOSE_BUTTON",
        ".ant-modal-close",
        "Кнопка закрытия модального окна",
        project="common",
        component="modal",
    )

    locator_registry.add_locator(
        "COMMON_MODAL_TITLE",
        ".ant-modal-title",
        "Заголовок модального окна",
        project="common",
        component="modal",
    )

    # === КНОПКИ ===

    locator_registry.add_locator(
        "COMMON_ALL_BUTTONS",
        "button[aria-label]",
        "Все кнопки с aria-label",
        project="common",
        component="button",
    )

    locator_registry.add_locator(
        "COMMON_EXPLORE_PROJECT_BUTTON",
        "//span[text()='Explore Project']",
        "Кнопка Explore Project",
        project="common",
        component="button",
    )

    # === ПРОЕКТНЫЕ КАРТОЧКИ ===

    locator_registry.add_locator(
        "COMMON_PROJECT_INFO_WINDOW",
        'div.ant-card[class*="_projectInfo"]',
        "Информационное окно проекта",
        project="common",
        component="project_card",
    )

    locator_registry.add_locator(
        "COMMON_PROJECT_CARD",
        "div.ant-card",
        "Карточка проекта",
        project="common",
        component="project_card",
    )


# Регистрируем локаторы при импорте
register_common_locators()


class CommonLocators:
    """Удобный доступ к общим локаторам."""

    def get(self, name: str, use_fallback: bool = False) -> str:
        """Получить локатор по имени."""
        return locator_registry.get_locator(name, use_fallback)

    def get_modal_locators(self) -> dict:
        """Получить все локаторы модальных окон."""
        return locator_registry.get_component_locators("modal")

    def get_button_locators(self) -> dict:
        """Получить все локаторы кнопок."""
        return locator_registry.get_component_locators("button")

    def get_map_locators(self) -> dict:
        """Получить все локаторы карты."""
        return locator_registry.get_component_locators("map")


# Экспортируем объект
common_locators = CommonLocators()
