import os

import allure
import pytest


@allure.feature("Qube - Проект Elire")
@allure.story("Навигация по зданиям, этажам и апартаментам")
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.ui
@pytest.mark.flaky(reruns=3, reruns_delay=4)
def test_elire_building_floor_apartment_navigation(map_page):
    """Тест навигации по зданиям, этажам и апартаментам проекта Elire."""

    # Получаем окружение для условной логики
    env = os.getenv("TEST_ENVIRONMENT", "prod")

    with allure.step("Открываем карту и переходим к проекту Elire"):
        map_page.open(route_type="map")
        map_page.click_project_on_map("elire")

    with allure.step("Кликаем на Residences"):
        map_page.elire.click_on_residences_button()

        map_page.assert_element_visible(
            map_page.project_locators.Elire.RESIDENCES_BUTTON,
            "Кнопка Residences не отображается после клика",
        )

        # Обрабатываем модальное окно авторизации только на PROD (на DEV авторизации нет)
        if env == "prod":
            map_page.handle_auth_modal_if_present()

    with allure.step("Кликаем на Start 3D Experience"):
        start_3d_button = (
            map_page.project_locators.Elire.START3DEXPREINCE_1BEDROOM_RESIDENCE
        )

        # Умное ожидание появления кнопки (на PROD может потребоваться больше времени из-за авторизации)
        timeout = 20000 if env == "prod" else 10000
        map_page.page.wait_for_selector(
            start_3d_button, state="visible", timeout=timeout
        )
        map_page.click(start_3d_button)

        map_page.assert_element_visible(
            start_3d_button, "Кнопка Start 3D Experience не найдена после клика"
        )

    # Проверяем URL здания
    map_page.page.wait_for_url("**/elire/configuration/1br-residence", timeout=10000)
    current_url = map_page.get_current_url()
    allure.attach(
        f"URL после выбора 1 Bedroom Residence: {current_url}", name="Building URL"
    )

    # Дополнительные шаги для Elire можно добавить здесь
    with allure.step("Проверяем финальный URL"):
        final_url = map_page.get_current_url()
        allure.attach(f"Финальный URL: {final_url}", name="Final URL")

        map_page.assert_url_contains(
            "/elire/configuration/1br-residence",
            "Не перешли на страницу конфигурации 1 Bedroom Residence",
        )
