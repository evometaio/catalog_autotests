import allure
import pytest


@allure.feature("Wellcube - Проект Tranquil")
@allure.story("Карта")
@pytest.mark.smoke
@pytest.mark.ui
def test_tranquil_map_page(wellcube_page):
    """Тест карты проекта Wellcube (Tranquil)."""
    with allure.step("Открываем карту Wellcube (Tranquil)"):
        wellcube_page.open(route_type="map")
        wellcube_page.check_map_loaded()

    with allure.step("Проверяем функциональность карты"):
        pass
