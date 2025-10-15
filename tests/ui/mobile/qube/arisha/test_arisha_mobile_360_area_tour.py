import allure
import pytest


@allure.feature("Qube - Проект Arisha (mobile)")
@allure.story("360тур по территории - Мобильная")
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.mobile
@pytest.mark.flaky(reruns=2, reruns_delay=4)
def test_arisha_mobile_360_area_tour(mobile_page):
    """Тест 360 Area Tour для проекта Arisha на мобильном устройстве."""
    with allure.step("Открываем карту"):
        mobile_page.open(route_type="map")

    with allure.step("Кликаем на проект Arisha на карте"):
        mobile_page.mobile_map.click_project("arisha")

    with allure.step("Кликаем на Explore Project"):
        mobile_page.mobile_map.click_explore_project("arisha")

    with allure.step("Кликаем на кнопку 360 Area Tour"):
        mobile_page.area_tour_360.click_360_button()

    with allure.step("Проверяем отображение модального окна 360 Area Tour"):
        mobile_page.area_tour_360.verify_modal_displayed()

    with allure.step("Проверяем наличие контента в модальном окне"):
        mobile_page.area_tour_360.verify_content()

    with allure.step("Закрываем модальное окно 360 Area Tour"):
        mobile_page.area_tour_360.close_modal()

    with allure.step("Проверяем адаптивность на мобильном устройстве"):
        mobile_page.check_mobile_viewport_adaptation()
