import allure
import pytest


@allure.feature("Qube - Проект Arisha")
@allure.story("360 тур по территории")
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.ui
@pytest.mark.flaky(reruns=2, reruns_delay=2)
@pytest.mark.parametrize("route_type", ["map", "agent", "client"])
def test_arisha_360_area_tour(arisha_page, route_type):
    """Тест 360 Area Tour для проекта Arisha на всех роутах."""
    with allure.step(f"Открываем страницу {route_type}"):
        arisha_page.open(route_type=route_type)

    with allure.step("Кликаем на проект Arisha"):
        arisha_page.map.navigate_to_project("arisha")

    with allure.step("Кликаем на кнопку 360 Area Tour"):
        arisha_page.area_tour_360.click_360_button()

    with allure.step("Проверяем отображение модального окна 360 Area Tour"):
        arisha_page.area_tour_360.verify_modal_displayed()

    with allure.step("Проверяем наличие контента в модальном окне"):
        arisha_page.area_tour_360.verify_content()

    with allure.step("Закрываем модальное окно 360 Area Tour"):
        arisha_page.area_tour_360.close_modal()
