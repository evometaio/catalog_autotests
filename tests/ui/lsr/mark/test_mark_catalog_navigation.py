import os

import allure
import pytest


@allure.feature("LSR - Проект MARK")
@allure.story("Навигация в каталог")
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.ui
@pytest.mark.skipif(
    os.getenv("TEST_ENVIRONMENT", "prod") != "dev",
    reason="Тест запускается только на dev окружении",
)
def test_mark_catalog_navigation(mark_page):
    """Тест перехода в каталог квартир для проекта MARK."""
    with allure.step("Открываем главную страницу MARK"):
        mark_page.open()

    with allure.step("Кликаем на кнопку All units для перехода на catalog2d"):
        mark_page.click_all_units_button()

    with allure.step("Проверяем наличие кнопок квартир в каталоге"):
        property_buttons = mark_page.page.locator(
            mark_page.project_locators.PROPERTY_INFO_PRIMARY_BUTTON
        )
        property_buttons.first.wait_for(state="attached", timeout=10000)
        assert property_buttons.count() > 0, "Не найдено кнопок квартир в каталоге"
