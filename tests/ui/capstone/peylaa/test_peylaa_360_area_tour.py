import allure
import pytest


@allure.feature("Capstone - Проект Peylaa")
@allure.story("360-градусный тур по территории")
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.ui
def test_peylaa_360_area_tour(capstone_project_page):
    """Тест 360 Area Tour для проекта Peylaa."""
    with allure.step("Открываем карту Capstone"):
        capstone_project_page.open()

    with allure.step("Кликаем на проект Peylaa"):
        capstone_project_page.click_project_on_map("peylaa")

    with allure.step("Кликаем на кнопку Area tour"):
        capstone_project_page.click_360_area_tour_button()

    with allure.step("Проверяем отображение модального окна 360 Area Tour"):
        capstone_project_page.verify_360_area_tour_modal_displayed()

    with allure.step("Проверяем наличие контента в модальном окне"):
        capstone_project_page.verify_360_area_tour_content()
