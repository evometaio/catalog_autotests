"""
Локаторы для проектов Wellcube (Tranquil).
"""

from ..base import locator_registry


def register_wellcube_locators():
    """Регистрирует все локаторы для проектов Wellcube."""

    # === TRANQUIL ===

    locator_registry.add_locator(
        "TRANQUIL_MAP_LOCATOR",
        'div[aria-label*="Tranquil"], div[aria-label*="TRANQUIL"]',
        "Локатор проекта Tranquil на карте",
        project="tranquil",
        component="map",
    )

    locator_registry.add_locator(
        "TRANQUIL_FRACTION_OWNERSHIP_BUTTON",
        '(//button[@data-test-id="property-info-primary-button-1102 A"])[2]',
        "Кнопка Fraction Ownership Offer для Tranquil",
        project="tranquil",
        component="button",
    )

    locator_registry.add_locator(
        "TRANQUIL_AMENITIES_MODAL",
        ".ant-modal-content",
        "Модальное окно amenities для Tranquil",
        project="tranquil",
        component="modal",
    )

    locator_registry.add_locator(
        "TRANQUIL_AMENITIES_TITLE",
        ".ant-modal-title",
        "Заголовок модального окна amenities",
        project="tranquil",
        component="modal",
    )

    locator_registry.add_locator(
        "TRANQUIL_AMENITIES_CLOSE_BUTTON",
        ".ant-modal-close",
        "Кнопка закрытия модального окна amenities",
        project="tranquil",
        component="modal",
    )

    # === ОБЩИЕ ЛОКАТОРЫ WELLCUBE ===

    locator_registry.add_locator(
        "WELLCUBE_AMENITIES_SLIDER",
        ".ant-carousel",
        "Слайдер amenities для Wellcube",
        project="wellcube",
        component="slider",
    )

    locator_registry.add_locator(
        "WELLCUBE_AMENITIES_SLIDER_IMAGES",
        ".ant-carousel .ant-carousel-item img",
        "Изображения в слайдере amenities",
        project="wellcube",
        component="slider",
    )

    locator_registry.add_locator(
        "WELLCUBE_AMENITIES_SLIDER_INDICATORS",
        ".ant-carousel .ant-carousel-dots li",
        "Индикаторы слайдера amenities",
        project="wellcube",
        component="slider",
    )


# Регистрируем локаторы при импорте
register_wellcube_locators()


class WellcubeLocators:
    """Удобный доступ к локаторам Wellcube проектов."""

    def get(self, name: str, use_fallback: bool = False) -> str:
        """Получить локатор по имени."""
        return locator_registry.get_locator(name, use_fallback)

    def get_tranquil_locators(self) -> dict:
        """Получить все локаторы Tranquil."""
        return locator_registry.get_project_locators("tranquil")

    def get_common_locators(self) -> dict:
        """Получить общие локаторы Wellcube."""
        return locator_registry.get_project_locators("wellcube")


# Экспортируем объект
wellcube_locators = WellcubeLocators()
