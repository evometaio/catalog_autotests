import allure
import pytest


@allure.feature("Qube - Проект Arisha")
@allure.story("Навигация по зданиям, этажам и апартаментам")
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.ui
def test_arisha_building_floor_apartment_navigation(map_page):
    """Тест навигации по зданиям, этажам и апартаментам проекта Arisha."""

    with allure.step("Открываем карту и переходим к проекту Arisha"):
        map_page.open(route_type="map")
        map_page.click_project_on_map("arisha")

    with allure.step("Выбираем здание 1"):
        building_url = map_page.project.navigate_to_building(building_number=1)
        map_page.assert_url_contains("/building/1", "Не перешли на страницу здания 1")

    with allure.step("Выбираем этаж 1"):
        floor_url = map_page.project.navigate_to_floor(floor_number=1)
        map_page.assert_url_contains("/floor/1/1", "Не перешли на страницу этажа 1")

    with allure.step("Кликаем на апартамент на этаже 1"):
        apartment_clicked = map_page.project.click_apartment_on_floor()
        map_page.assert_that(apartment_clicked, "Не удалось кликнуть на апартамент на этаже 1")

    with allure.step("Переходим на этаж 2"):
        floor_2_url = map_page.project.navigate_to_floor_direct(
            project_name="arisha", building_number=1, floor_number=2
        )
        map_page.assert_url_contains("/floor/1/2", "Не перешли на страницу этажа 2")

    with allure.step("Кликаем на апартамент на этаже 2"):
        apartment_clicked_2 = map_page.project.click_apartment_on_floor()
        map_page.assert_that(apartment_clicked_2, "Не удалось кликнуть на апартамент на этаже 2")
