import allure
import pytest


@allure.feature("Capstone - Проект Peylaa")
@allure.story("Проверка карты")
@pytest.mark.smoke
@pytest.mark.ui
def test_capstone_map_page(main_page):
    """Тест проверки карты проекта Capstone (Peylaa)."""
    # TODO: Реализовать тест после создания фикстур для Capstone
    with allure.step("Открываем карту проекта Capstone"):
        main_page.open(route_type="map")

    with allure.step("Проверяем загрузку карты"):
        # main_page.check_map_loaded()
        pass

    with allure.step("Проверяем проекты на карте"):
        # TODO: Добавить логику проверки проектов Capstone
        pass
