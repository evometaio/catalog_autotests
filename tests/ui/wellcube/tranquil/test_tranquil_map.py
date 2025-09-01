import allure
import pytest


@allure.feature("Wellcube - Проект Tranquil")
@allure.story("Карта")
@pytest.mark.smoke
@pytest.mark.ui
def test_tranquil_map_page(wellcube_map_page):
    """Тест карты проекта Wellcube (Tranquil)."""
    with allure.step("Открываем карту Wellcube (Tranquil)"):
        wellcube_map_page.open_map_page()
        wellcube_map_page.check_map_loaded()

    with allure.step("Проверяем функциональность карты"):
        pass