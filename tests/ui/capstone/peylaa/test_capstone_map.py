import allure
import pytest


@allure.feature("Capstone - Проект Peylaa")
@allure.story("Проверка карты")
@pytest.mark.smoke
@pytest.mark.ui
def test_capstone_map_page():
    """Тест проверки карты проекта Capstone (Peylaa)."""
    # TODO: Реализовать тест после создания фикстур для Capstone
    with allure.step("Открываем карту проекта Capstone"):
        # capstone_map_page.open_map_page()
        pass

    with allure.step("Проверяем загрузку карты"):
        # capstone_map_page.check_map_loaded()
        pass

    with allure.step("Проверяем проекты на карте"):
        # TODO: Добавить логику проверки проектов Capstone
        pass
