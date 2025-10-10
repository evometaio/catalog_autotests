import allure
import pytest


@allure.feature("Capstone - Проект Peylaa (mobile)")
@allure.story("Проверка карты - Мобильная")
@pytest.mark.smoke
@pytest.mark.mobile
@pytest.mark.skip(reason="Реализовать")
def test_capstone_mobile_map_page(mobile_page):
    """Тест проверки карты проекта Capstone (Peylaa) на мобильном устройстве."""
    # TODO: Реализовать тест после создания фикстур для Capstone
    with allure.step("Открываем карту проекта Capstone"):
        mobile_page.open(route_type="map")

    with allure.step("Проверяем загрузку карты"):
        # mobile_page.check_map_loaded()
        pass

    with allure.step("Проверяем проекты на карте"):
        # TODO: Добавить логику проверки проектов Capstone
        pass

    with allure.step("Проверяем адаптивность на мобильном устройстве"):
        mobile_page.check_mobile_viewport_adaptation()
