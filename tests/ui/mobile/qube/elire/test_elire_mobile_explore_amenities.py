import allure
import pytest


@allure.feature("Qube - Проект Elire (mobile)")
@allure.story("Explore Amenities - Мобильная")
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.mobile
def test_elire_mobile_explore_amenities(mobile_page):
    """Тест Explore Amenities для проекта Elire на мобильном устройстве."""

    with allure.step("Открываем карту"):
        mobile_page.open(route_type="map")

    with allure.step("Кликаем на проект Elire"):
        mobile_page.click_mobile_project_on_map("elire")

    with allure.step("Кликаем на Explore Project"):
        mobile_page.click_mobile_explore_project_button("elire")

    mobile_page.click_mobile_services_amenities_button()

    mobile_page.verify_elire_services_modal_displayed()

    mobile_page.verify_elire_services_modal_title()

    mobile_page.navigate_elire_services_slider()

    mobile_page.close_elire_services_modal()

    with allure.step("Проверяем адаптивность на мобильном устройстве"):
        mobile_page.check_mobile_viewport_adaptation()
