import allure
import pytest


@allure.feature("Capstone - Проект Peylaa (mobile)")
@allure.story("360-градусный тур по территории - Мобильная")
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.mobile
def test_peylaa_mobile_360_area_tour(mobile_page):
    """Тест 360 Area Tour для проекта Peylaa на мобильном устройстве."""
    with allure.step("Открываем карту Capstone"):
        mobile_page.open(route_type="map")

    with allure.step("Кликаем на проект Peylaa"):
        mobile_page.mobile_map.click_project("peylaa")

    with allure.step("Кликаем на Explore Project"):
        mobile_page.mobile_map.click_explore_project("peylaa")

    with allure.step("Кликаем на кнопку Area tour"):
        mobile_page.area_tour_360.click_360_button()
        mobile_page.browser.wait_for_timeout(5000)

    with allure.step("Проверяем отображение модального окна 360 Area Tour"):
        mobile_page.area_tour_360.verify_modal_displayed()
        mobile_page.browser.wait_for_timeout(5000)

    with allure.step("Проверяем наличие контента в модальном окне"):
        mobile_page.area_tour_360.verify_content()
        mobile_page.browser.wait_for_timeout(5000)

    with allure.step("Проверяем адаптивность на мобильном устройстве"):
        mobile_page.check_mobile_viewport_adaptation()
