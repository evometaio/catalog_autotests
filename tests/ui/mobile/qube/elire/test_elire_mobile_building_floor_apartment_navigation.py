import os

import allure
import pytest


@allure.feature("Qube - Проект Elire (mobile)")
@allure.story("Навигация по зданиям, этажам и апартаментам - Мобильная")
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.mobile
def test_elire_mobile_building_floor_apartment_navigation(mobile_page):
    """Тест навигации по зданиям, этажам и апартаментам проекта Elire на мобильном устройстве."""

    # Получаем окружение для условной логики
    env = os.getenv("TEST_ENVIRONMENT", "prod")

    with allure.step("Открываем карту и переходим к проекту Elire"):
        mobile_page.open(route_type="map")
        mobile_page.click_mobile_project_on_map("elire")

    with allure.step("Кликаем на Explore Project"):
        mobile_page.click_mobile_explore_project_button("elire")

    mobile_page.click_mobile_explore_residences_button()

    # Обрабатываем модальное окно авторизации только на PROD (на DEV авторизации нет)
    if env == "prod":
        mobile_page.handle_auth_modal_if_present()

    mobile_page.click_mobile_start_3d_experience_button()

    with allure.step("Проверяем переход на страницу конфигурации"):
        mobile_page.page.wait_for_url(
            "**/elire/configuration/1br-residence", timeout=10000
        )
        mobile_page.assert_url_contains(
            "/elire/configuration/1br-residence",
            "Не перешли на страницу конфигурации 1 Bedroom Residence",
        )

    with allure.step("Проверяем адаптивность на мобильном устройстве"):
        mobile_page.check_mobile_viewport_adaptation()
