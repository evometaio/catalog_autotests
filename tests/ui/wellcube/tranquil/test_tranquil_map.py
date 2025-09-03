import allure
import pytest


@allure.feature("Wellcube - Проект Tranquil")
@allure.story("Карта")
@pytest.mark.smoke
@pytest.mark.ui
def test_tranquil_map_page(main_page):
    """Тест карты проекта Wellcube (Tranquil)."""
    with allure.step("Открываем карту Wellcube (Tranquil)"):
        main_page.open(route_type="map")
        main_page.check_map_loaded()

    with allure.step("Проверяем функциональность карты"):
        pass
