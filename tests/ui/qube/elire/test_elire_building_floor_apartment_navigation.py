import os

import allure
import pytest


@allure.feature("Qube - Проект Elire")
@allure.story("Навигация по зданиям, этажам и апартаментам")
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.ui
@pytest.mark.flaky(reruns=3, reruns_delay=2)
@pytest.mark.parametrize("route_type", ["map", "agent", "client"])
def test_elire_building_floor_apartment_navigation(elire_page, route_type):
    """Тест навигации по зданиям, этажам и апартаментам проекта Elire на всех роутах."""

    # Получаем окружение для условной логики
    env = os.getenv("TEST_ENVIRONMENT", "prod")

    with allure.step(f"Открываем страницу {route_type} и переходим к проекту Elire"):
        elire_page.open(route_type=route_type)
        elire_page.map.navigate_to_project("elire")

    with allure.step("Кликаем на Residences"):
        elire_page.click_residences_button()

        elire_page.assertions.assert_element_visible(
            elire_page.project_locators.RESIDENCES_BUTTON,
            "Кнопка Residences не отображается после клика",
        )

        # Обрабатываем модальное окно авторизации только на PROD (на DEV авторизации нет)
        if env == "prod":
            elire_page.handle_auth_modal_if_present()

    with allure.step("Кликаем на Start 3D Experience"):
        start_3d_button = (
            elire_page.project_locators.START3DEXPREINCE_1BEDROOM_RESIDENCE
        )

        # Умное ожидание появления кнопки (на PROD может потребоваться больше времени из-за авторизации)
        timeout = 20000 if env == "prod" else 10000
        elire_page.page.wait_for_selector(
            start_3d_button, state="visible", timeout=timeout
        )
        elire_page.browser.click(start_3d_button)

        elire_page.assertions.assert_element_visible(
            start_3d_button, "Кнопка Start 3D Experience не найдена после клика"
        )

    # Проверяем URL здания
    elire_page.page.wait_for_url("**/elire/configuration/1br-residence", timeout=10000)
    current_url = elire_page.get_current_url()
    allure.attach(
        f"URL после выбора 1 Bedroom Residence: {current_url}", name="Building URL"
    )

    # Дополнительные шаги для Elire можно добавить здесь
    with allure.step("Проверяем финальный URL"):
        final_url = elire_page.get_current_url()
        allure.attach(f"Финальный URL: {final_url}", name="Final URL")

        elire_page.assertions.assert_url_contains(
            "/elire/configuration/1br-residence",
            "Не перешли на страницу конфигурации 1 Bedroom Residence",
        )
