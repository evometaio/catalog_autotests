import allure
import pytest


@allure.feature("Qube - Проект Elire")
@allure.story("Навигация по зданиям, этажам и апартаментам")
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.ui
def test_elire_building_floor_apartment_navigation(map_page):
    """Тест навигации по зданиям, этажам и апартаментам проекта Elire."""

    with allure.step("Открываем карту и переходим к проекту Elire"):
        map_page.open(route_type="map")
        map_page.click_project_on_map("elire")

    with allure.step("Кликаем на Residences"):
        map_page.elire.click_on_residences_button()
        assert map_page.is_visible(
            map_page.project_locators.Elire.RESIDENCES_BUTTON
        ), "Не найдена кнопка Residences"

    with allure.step("Кликаем на Start 3D Experience"):
        map_page.click(
            map_page.project_locators.Elire.START3DEXPREINCE_1BEDROOM_RESIDENCE
        )
        assert map_page.is_visible(
            map_page.project_locators.Elire.START3DEXPREINCE_1BEDROOM_RESIDENCE
        ), "Не найдена кнопка Start 3D Experience"

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

        # Проверяем, что мы на правильной странице
        assert (
            "/elire/configuration/1br-residence" in final_url
        ), f"Не на странице 1 Bedroom Residence. URL: {final_url}"
