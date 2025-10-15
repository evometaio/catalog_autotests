import allure
import pytest


@allure.feature("Capstone - Проект Peylaa")
@allure.story("360-градусный тур по территории")
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.ui
def test_peylaa_360_area_tour(peylaa_page):
    """Тест 360 Area Tour для проекта Peylaa."""
    with allure.step("Открываем карту Capstone"):
        peylaa_page.open()

    with allure.step("Кликаем на проект Peylaa"):
        peylaa_page.map.navigate_to_project("peylaa")

    with allure.step("Кликаем на кнопку Area tour"):
        peylaa_page.area_tour_360.click_360_button()

    with allure.step("Проверяем отображение модального окна 360 Area Tour"):
        peylaa_page.area_tour_360.verify_modal_displayed()

    with allure.step("Проверяем наличие контента в модальном окне"):
        peylaa_page.area_tour_360.verify_content()
