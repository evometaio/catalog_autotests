import os

import allure
import pytest


@allure.feature("Vibe - Проект Arsenal")
@allure.story("Навигация в каталог")
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.ui
@pytest.mark.skipif(
    os.getenv("TEST_ENVIRONMENT", "prod") != "dev",
    reason="Тест запускается только на dev окружении",
)
def test_arsenal_catalog_navigation(arsenal_page):
    """Тест перехода в каталог квартир для проекта Arsenal."""
    with allure.step("Открываем страницу map"):
        arsenal_page.open(route_type="map")

    with allure.step("Кликаем на кнопку All units для перехода на catalog2d"):
        arsenal_page.click_all_units_button()
        arsenal_page.assertions.assert_url_contains(
            "catalog_2d", "Не перешли на страницу каталога"
        )

    with allure.step("Проверяем наличие кнопок квартир в каталоге"):
        property_buttons = arsenal_page.page.locator(
            arsenal_page.project_locators.PROPERTY_INFO_PRIMARY_BUTTON
        )
        # Ждем появления хотя бы одной кнопки (может быть скрыта, но должна быть в DOM)
        property_buttons.first.wait_for(state="attached", timeout=10000)
        assert property_buttons.count() > 0, "Не найдено кнопок квартир в каталоге"
