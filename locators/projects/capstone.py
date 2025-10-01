"""
Локаторы для проектов Capstone (Peylaa).
"""

from ..base import locator_registry


def register_capstone_locators():
    """Регистрирует все локаторы для проектов Capstone."""

    # === PEYLAA ===

    locator_registry.add_locator(
        "PEYLAA_MAP_LOCATOR_DEV",
        'div[title="Peylaa"][aria-label="Peylaa"]',
        "Локатор проекта Peylaa на карте (DEV)",
        project="peylaa",
        component="map",
    )

    locator_registry.add_locator(
        "PEYLAA_MAP_LOCATOR_PROD",
        'div[aria-label*="Peylaa"]',
        "Локатор проекта Peylaa на карте (PROD)",
        project="peylaa",
        component="map",
    )

    locator_registry.add_locator(
        "PEYLAA_360_BUTTON",
        '[data-test-id="nav-rotation-view-controls-button"]',
        "Кнопка 360 Area Tour для Peylaa",
        project="peylaa",
        component="navigation",
    )

    # === ОБЩИЕ ЛОКАТОРЫ CAPSTONE ===

    locator_registry.add_locator(
        "CAPSTONE_360_MODAL",
        ".ant-modal-content",
        "Модальное окно 360 Area Tour для Capstone",
        project="capstone",
        component="modal",
    )

    locator_registry.add_locator(
        "CAPSTONE_360_CONTENT",
        '//img[contains(@class, "__react-image-turntable-img")] | //video | //canvas',
        "Контент в модальном окне 360 Area Tour",
        project="capstone",
        component="modal",
    )

    locator_registry.add_locator(
        "CAPSTONE_360_CLOSE_BUTTON",
        '//button[contains(@class, "close") and @aria-label="close"]',
        "Кнопка закрытия модального окна 360 Area Tour",
        project="capstone",
        component="modal",
    )


# Регистрируем локаторы при импорте
register_capstone_locators()


class CapstoneLocators:
    """Удобный доступ к локаторам Capstone проектов."""

    def get(self, name: str, use_fallback: bool = False) -> str:
        """Получить локатор по имени."""
        return locator_registry.get_locator(name, use_fallback)

    def get_peylaa_locators(self) -> dict:
        """Получить все локаторы Peylaa."""
        return locator_registry.get_project_locators("peylaa")

    def get_common_locators(self) -> dict:
        """Получить общие локаторы Capstone."""
        return locator_registry.get_project_locators("capstone")


# Экспортируем объект
capstone_locators = CapstoneLocators()
