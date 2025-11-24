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
    with allure.step("Открываем главную страницу Arsenal"):
        arsenal_page.open()

    with allure.step("Кликаем на проект Arsenal для перехода в каталог"):
        # Для Arsenal клик на проект сразу ведет в каталог
        project_button = arsenal_page.page.locator(
            '[data-test-id="nav-desktop-project-vibe"]'
        )
        project_button.wait_for(state="visible", timeout=10000)
        project_button.click()
        arsenal_page.page.wait_for_url("**/catalog_2d", timeout=10000)

    with allure.step("Проверяем наличие кнопок квартир в каталоге"):
        property_buttons = arsenal_page.page.locator(
            arsenal_page.project_locators.PROPERTY_INFO_PRIMARY_BUTTON
        )
        # Ждем появления хотя бы одной кнопки (может быть скрыта, но должна быть в DOM)
        property_buttons.first.wait_for(state="attached", timeout=10000)
        assert property_buttons.count() > 0, "Не найдено кнопок квартир в каталоге"
