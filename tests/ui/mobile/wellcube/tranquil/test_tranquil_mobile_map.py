import allure
import pytest


@allure.feature("Wellcube - Проект Tranquil (mobile)")
@allure.story("Карта - Мобильная")
@pytest.mark.smoke
@pytest.mark.mobile
@pytest.mark.skip(reason="Реализовать")
def test_tranquil_mobile_map_page(mobile_page):
    """Тест карты проекта Wellcube (Tranquil) на мобильном устройстве."""
    with allure.step("Открываем карту Wellcube (Tranquil)"):
        mobile_page.open(route_type="map")
        mobile_page.check_map_loaded()

    with allure.step("Проверяем функциональность карты"):
        pass

    with allure.step("Проверяем адаптивность на мобильном устройстве"):
        mobile_page.check_mobile_viewport_adaptation()
