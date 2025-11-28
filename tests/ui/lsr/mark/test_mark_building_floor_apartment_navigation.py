import allure
import pytest


@allure.feature("LSR - Проект MARK")
@allure.story("Навигация по зданиям, этажам и апартаментам")
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.ui
@pytest.mark.flaky(reruns=2, reruns_delay=2)
def test_mark_building_floor_apartment_navigation(mark_page):
    """Тест навигации по зданиям, этажам и апартаментам проекта MARK."""

    with allure.step("Открываем страницу MARK"):
        mark_page.open()

    with allure.step("Выбираем здание 1"):
        mark_page.navigate_to_building(building_number=1)
        mark_page.assertions.assert_url_contains(
            "/building/mark-k1", "Не перешли на страницу здания 1"
        )

    with allure.step("Выбираем этаж 6"):
        mark_page.navigate_to_floor(floor_number=6)
        mark_page.assertions.assert_url_contains(
            "/floor/mark-k1/6", "Не перешли на страницу этажа 6"
        )

    with allure.step("Кликаем на апартамент на этаже 6"):
        apartment_clicked = mark_page.navigation.click_apartment_on_floor()
        mark_page.assertions.assert_that(
            apartment_clicked, "Не удалось кликнуть на апартамент на этаже 6"
        )

    with allure.step("Переходим на этаж 7"):
        mark_page.navigate_to_floor(floor_number=7)
        mark_page.assertions.assert_url_contains(
            "/floor/mark-k1/7", "Не перешли на страницу этажа 7"
        )

    with allure.step("Кликаем на апартамент на этаже 7"):
        apartment_clicked_2 = mark_page.navigation.click_apartment_on_floor()
        mark_page.assertions.assert_that(
            apartment_clicked_2, "Не удалось кликнуть на апартамент на этаже 7"
        )
