import os

import allure
import pytest


@allure.feature("Qube - Проект Arisha")
@allure.story("360 Area Tour")
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.ui
@pytest.mark.skipif(
    os.getenv("TEST_ENVIRONMENT", "dev") == "prod",
    reason="тест временно отключен на PROD",
)
def test_arisha_360_area_tour(map_page):
    """Тест 360 Area Tour для проекта Arisha."""
    with allure.step("Открываем главную страницу"):
        map_page.open()

    with allure.step("Кликаем на проект Arisha"):
        map_page.click_project_on_map("arisha")

    with allure.step("Кликаем на кнопку 360 Area Tour"):
        map_page.click_360_area_tour_button()

    with allure.step("Проверяем отображение модального окна 360 Area Tour"):
        map_page.verify_360_area_tour_modal_displayed()

    with allure.step("Проверяем наличие контента в модальном окне"):
        map_page.verify_360_area_tour_content()

    with allure.step("Закрываем модальное окно 360 Area Tour"):
        map_page.close_360_area_tour_modal()
