import allure
import pytest


@allure.feature("Qube - Проект Arisha")
@allure.story("360-градусный тур по территории")
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.ui
@pytest.mark.flaky(reruns=2, reruns_delay=4)
def test_arisha_360_area_tour(arisha_page):
    """Тест 360 Area Tour для проекта Arisha."""
    with allure.step("Открываем главную страницу"):
        arisha_page.open(route_type="map")

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
