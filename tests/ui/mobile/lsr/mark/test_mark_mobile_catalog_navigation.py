"""Мобильный тест навигации в каталог для проекта MARK."""

import allure
import pytest


@allure.feature("LSR - Проект MARK (mobile)")
@allure.story("Навигация в каталог")
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.mobile
def test_mark_mobile_catalog_navigation(mark_page):
    """Тест перехода в каталог квартир MARK на мобильном устройстве."""
    with allure.step("Открываем главную страницу MARK (mobile)"):
        mark_page.open()

    with allure.step("Открываем мобильное меню"):
        menu_toggle = mark_page.page.locator(
            mark_page.project_locators.NAV_MOBILE_MENU_TOGGLE
        )
        menu_toggle.wait_for(state="visible", timeout=10000)
        menu_toggle.click()

    with allure.step("Кликаем на All units в мобильном меню"):
        catalog_button = mark_page.page.locator(
            mark_page.project_locators.NAV_MOBILE_CATALOG2D
        )
        catalog_button.wait_for(state="visible", timeout=10000)
        catalog_button.click()

    with allure.step("Проверяем наличие кнопок квартир в каталоге"):
        property_buttons = mark_page.page.locator(
            mark_page.project_locators.PROPERTY_INFO_PRIMARY_BUTTON
        )
        # Ждем, пока на странице появится хотя бы одна кнопка квартиры
        property_buttons.first.wait_for(state="attached", timeout=10000)
        assert (
            property_buttons.count() > 0
        ), "Не найдено кнопок квартир в каталоге на мобилке"
