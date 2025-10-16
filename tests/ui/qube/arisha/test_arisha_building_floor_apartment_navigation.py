import allure
import pytest


@allure.feature("Qube - Проект Arisha")
@allure.story("Навигация по зданиям, этажам и апартаментам")
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.ui
@pytest.mark.flaky(reruns=2, reruns_delay=2)
@pytest.mark.parametrize("route_type", ["map", "agent", "client"])
def test_arisha_building_floor_apartment_navigation(arisha_page, route_type):
    """Тест навигации по зданиям, этажам и апартаментам проекта Arisha на всех роутах."""

    with allure.step(f"Открываем страницу {route_type} и переходим к проекту Arisha"):
        arisha_page.open(route_type=route_type)
        arisha_page.map.navigate_to_project("arisha")

    with allure.step("Выбираем здание 1"):
        arisha_page.navigate_to_building(building_number=1)
        arisha_page.assertions.assert_url_contains(
            "/building/1", "Не перешли на страницу здания 1"
        )

    with allure.step("Выбираем этаж 1"):
        arisha_page.navigate_to_floor(floor_number=1)
        arisha_page.assertions.assert_url_contains(
            "/floor/1/1", "Не перешли на страницу этажа 1"
        )

    with allure.step("Кликаем на апартамент на этаже 1"):
        apartment_clicked = arisha_page.navigation.click_apartment_on_floor()
        arisha_page.assertions.assert_that(
            apartment_clicked, "Не удалось кликнуть на апартамент на этаже 1"
        )

    with allure.step("Переходим на этаж 2"):
        arisha_page.navigate_to_floor(floor_number=2)
        arisha_page.assertions.assert_url_contains(
            "/floor/1/2", "Не перешли на страницу этажа 2"
        )

    with allure.step("Кликаем на апартамент на этаже 2"):
        apartment_clicked_2 = arisha_page.navigation.click_apartment_on_floor()
        arisha_page.assertions.assert_that(
            apartment_clicked_2, "Не удалось кликнуть на апартамент на этаже 2"
        )
