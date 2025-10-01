"""
Локаторы для проектов Qube (Arisha, Elire, Cubix).
"""

from ..base import locator_registry


# Регистрируем локаторы для Qube проектов
def register_qube_locators():
    """Регистрирует все локаторы для проектов Qube."""

    # === ARISHA ===

    # Основные локаторы Arisha
    locator_registry.add_locator(
        "ARISHA_MAP_LOCATOR",
        'div[aria-label*="ARISHA TERACCES"], div[aria-label*="Arisha"], div[aria-label*="ARISHA"]',
        "Локатор проекта Arisha на карте",
        project="arisha",
        component="map",
    )

    locator_registry.add_locator(
        "ARISHA_360_BUTTON",
        '[data-test-id="nav-rotation-view-controls-button"]',
        "Кнопка 360 Area Tour для Arisha",
        project="arisha",
        component="navigation",
    )

    # Apartment Widget для Arisha
    locator_registry.add_locator(
        "ARISHA_APARTMENT_2D_BUTTON",
        'button:has-text("2D")',
        "Кнопка переключения в 2D режим",
        project="arisha",
        component="apartment_widget",
    )

    locator_registry.add_locator(
        "ARISHA_APARTMENT_3D_BUTTON",
        'button:has-text("3D")',
        "Кнопка переключения в 3D режим",
        project="arisha",
        component="apartment_widget",
    )

    locator_registry.add_locator(
        "ARISHA_APARTMENT_NEXT_ARROW",
        'button[aria-label*="next"], .next-button, [class*="next"]',
        "Кнопка следующего слайда в виджете апартамента",
        project="arisha",
        component="apartment_widget",
    )

    locator_registry.add_locator(
        "ARISHA_APARTMENT_SCENE_INDICATOR",
        '[class*="indicator"], [class*="dot"], [class*="scene"]',
        "Индикатор сцены в виджете апартамента",
        project="arisha",
        component="apartment_widget",
    )

    # === ELIRE ===

    locator_registry.add_locator(
        "ELIRE_MAP_LOCATOR",
        'div[aria-label="Elire"]',
        "Локатор проекта Elire на карте",
        project="elire",
        component="map",
    )

    locator_registry.add_locator(
        "ELIRE_RESIDENCES_BUTTON",
        '[data-test-id="nav-desktop-catalog2d"]',
        "Кнопка Residences для Elire",
        project="elire",
        component="navigation",
    )

    locator_registry.add_locator(
        "ELIRE_AMENITIES_MODAL",
        ".ant-modal-content",
        "Модальное окно amenities для Elire",
        project="elire",
        component="modal",
    )

    locator_registry.add_locator(
        "ELIRE_AMENITIES_TITLE",
        ".ant-modal-content h3._title_6w0b9_41",
        "Заголовок модального окна amenities",
        project="elire",
        component="modal",
    )

    locator_registry.add_locator(
        "ELIRE_AMENITIES_CLOSE_BUTTON",
        ".ant-modal-close",
        "Кнопка закрытия модального окна amenities",
        project="elire",
        component="modal",
    )

    locator_registry.add_locator(
        "ELIRE_AMENITIES_SLIDER",
        ".ant-carousel",
        "Слайдер в модальном окне amenities",
        project="elire",
        component="slider",
    )

    locator_registry.add_locator(
        "ELIRE_AMENITIES_SLIDER_IMAGES",
        ".ant-carousel .ant-carousel-item img",
        "Изображения в слайдере amenities",
        project="elire",
        component="slider",
    )

    locator_registry.add_locator(
        "ELIRE_AMENITIES_SLIDER_INDICATORS",
        ".ant-carousel .ant-carousel-dots li",
        "Индикаторы слайдера amenities",
        project="elire",
        component="slider",
    )

    # === CUBIX ===

    locator_registry.add_locator(
        "CUBIX_MAP_LOCATOR",
        'div[aria-label*="CUBIX RESIDENCE"], div[aria-label*="Cubix"], div[aria-label*="CUBIX"]',
        "Локатор проекта Cubix на карте",
        project="cubix",
        component="map",
    )

    # === ОБЩИЕ ЛОКАТОРЫ QUBE ===

    locator_registry.add_locator(
        "QUBE_BUILDING_NAV_BUTTON",
        '[data-test-id="nav-desktop-building"]',
        "Кнопка навигации по зданиям",
        project="qube",
        component="navigation",
    )

    locator_registry.add_locator(
        "QUBE_FLOOR_NAV_BUTTON",
        '[data-test-id="nav-desktop-floor"]',
        "Кнопка навигации по этажам",
        project="qube",
        component="navigation",
    )

    locator_registry.add_locator(
        "QUBE_ALL_UNITS_BUTTON",
        '[data-test-id="nav-desktop-catalog2d-standalone"]',
        "Кнопка 'All units' для просмотра всех единиц",
        project="qube",
        component="navigation",
    )

    locator_registry.add_locator(
        "QUBE_FLOOR_PLAN_APARTMENTS",
        'svg [class*="apartment"], [class*="apartment"], [data-test-id*="apartment"]',
        "Апартаменты на плане этажа",
        project="qube",
        component="floor_plan",
    )

    locator_registry.add_locator(
        "QUBE_360_MODAL",
        ".ant-modal-content",
        "Модальное окно 360 Area Tour",
        project="qube",
        component="modal",
    )

    locator_registry.add_locator(
        "QUBE_360_CONTENT",
        '//img[contains(@class, "__react-image-turntable-img")] | //video | //canvas',
        "Контент в модальном окне 360 Area Tour",
        project="qube",
        component="modal",
    )

    locator_registry.add_locator(
        "QUBE_360_CLOSE_BUTTON",
        '//button[contains(@class, "close") and @aria-label="close"]',
        "Кнопка закрытия модального окна 360 Area Tour",
        project="qube",
        component="modal",
    )


# Регистрируем локаторы при импорте
register_qube_locators()


# Создаем удобный объект для доступа к локаторам
class QubeLocators:
    """Удобный доступ к локаторам Qube проектов."""

    def get(self, name: str, use_fallback: bool = False) -> str:
        """Получить локатор по имени."""
        return locator_registry.get_locator(name, use_fallback)

    def get_arisha_locators(self) -> dict:
        """Получить все локаторы Arisha."""
        return locator_registry.get_project_locators("arisha")

    def get_elire_locators(self) -> dict:
        """Получить все локаторы Elire."""
        return locator_registry.get_project_locators("elire")

    def get_cubix_locators(self) -> dict:
        """Получить все локаторы Cubix."""
        return locator_registry.get_project_locators("cubix")

    def get_common_locators(self) -> dict:
        """Получить общие локаторы Qube."""
        return locator_registry.get_project_locators("qube")


# Экспортируем объект
qube_locators = QubeLocators()
