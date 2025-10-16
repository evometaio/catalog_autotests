import allure
import pytest


@allure.feature("Qube - Проект Arisha (mobile)")
@allure.story("360тур по территории - Мобильная")
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.mobile
@pytest.mark.flaky(reruns=2, reruns_delay=2)
@pytest.mark.parametrize("route_type", ["map", "agent", "client"])
def test_arisha_mobile_360_area_tour(mobile_page, route_type):
    """Тест 360 Area Tour для проекта Arisha на мобильном устройстве на всех роутах."""
    with allure.step(f"Открываем страницу {route_type}"):
        mobile_page.open(route_type=route_type)

    with allure.step("Кликаем на проект Arisha на карте"):
        mobile_page.mobile_map.click_project("arisha")

    with allure.step("Кликаем на Explore Project"):
        mobile_page.mobile_map.click_explore_project("arisha")

    with allure.step("Кликаем на кнопку 360 Area Tour"):
        mobile_page.click_360_area_tour_button()

    with allure.step("Проверяем отображение модального окна 360 Area Tour"):
        mobile_page.area_tour_360.verify_modal_displayed()

    with allure.step("Проверяем наличие контента в модальном окне"):
        mobile_page.area_tour_360.verify_content()

    with allure.step("Закрываем модальное окно 360 Area Tour"):
        mobile_page.area_tour_360.close_modal()

    with allure.step("Проверяем адаптивность на мобильном устройстве"):
        mobile_page.check_mobile_viewport_adaptation()
