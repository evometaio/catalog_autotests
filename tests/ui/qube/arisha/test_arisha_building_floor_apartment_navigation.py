import os

import allure
import pytest


@allure.feature("Qube - Проект Arisha")
@allure.story("Навигация по зданиям, этажам и апартаментам")
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.ui
@pytest.mark.flaky(reruns=2, reruns_delay=4)
def test_arisha_building_floor_apartment_navigation(map_page):
    """Тест навигации по зданиям, этажам и апартаментам проекта Arisha."""

    with allure.step("Открываем карту и переходим к проекту Arisha"):
        map_page.open(route_type="map")
        map_page.click_project_on_map("arisha")

    with allure.step("Выбираем здание 1"):
        map_page.click(map_page.project_locators.BUILDING_NAV_BUTTON)
        map_page.click(map_page.project_locators.BUILDING_1_BUTTON)

        # Проверяем URL здания
        map_page.page.wait_for_url("**/building/1", timeout=10000)
        current_url = map_page.get_current_url()
        allure.attach(f"URL после выбора здания 1: {current_url}", name="Building URL")

    with allure.step("Выбираем этаж 1"):
        map_page.click(map_page.project_locators.FLOOR_NAV_BUTTON)
        map_page.click(map_page.project_locators.FLOOR_1_BUTTON)

        # Проверяем URL этажа
        map_page.page.wait_for_url("**/floor/1/1", timeout=10000)
        current_url = map_page.get_current_url()
        allure.attach(f"URL после выбора этажа 1: {current_url}", name="Floor URL")

    with allure.step("Ищем и кликаем на доступный апартамент на этаже 1"):
        # Ждем загрузки плана этажа
        map_page.page.wait_for_selector(
            map_page.project_locators.FLOOR_PLAN_APARTMENTS, timeout=10000
        )

        apartment_elements = map_page.page.locator(
            map_page.project_locators.FLOOR_PLAN_APARTMENTS
        )
        apartment_count = apartment_elements.count()
        allure.attach(
            f"Найдено апартаментов на этаже: {apartment_count}", name="Apartment Count"
        )

        # Кликаем на первый доступный апартамент
        apartment_clicked = map_page.click_available_apartment()
        if not apartment_clicked:
            allure.attach(
                "Не удалось найти доступный апартамент на этаже 1", name="Warning"
            )
            # Пропускаем тест, если нет доступных апартаментов
            pytest.skip("Нет доступных апартаментов на этаже 1")

    with allure.step("Возвращаемся к плану этажа"):
        map_page.page.go_back()
        map_page.page.wait_for_url("**/floor/1/1", timeout=10000)

    with allure.step("Переходим на этаж 2"):
        map_page.click(map_page.project_locators.FLOOR_NAV_BUTTON)
        map_page.click(map_page.project_locators.FLOOR_2_BUTTON)

        # Проверяем URL этажа 2
        map_page.page.wait_for_url("**/floor/1/2", timeout=10000)
        current_url = map_page.get_current_url()
        allure.attach(f"URL после выбора этажа 2: {current_url}", name="Floor 2 URL")

    with allure.step("Ищем и кликаем на доступный апартамент на этаже 2"):
        # Ждем загрузки плана этажа 2
        map_page.page.wait_for_selector(
            map_page.project_locators.FLOOR_PLAN_APARTMENTS, timeout=10000
        )

        apartment_elements_2 = map_page.page.locator(
            map_page.project_locators.FLOOR_PLAN_APARTMENTS
        )
        apartment_count_2 = apartment_elements_2.count()
        allure.attach(
            f"Найдено апартаментов на этаже 2: {apartment_count_2}",
            name="Apartment Count Floor 2",
        )

        # Кликаем на первый доступный апартамент
        apartment_clicked_2 = map_page.click_available_apartment()
        if not apartment_clicked_2:
            allure.attach(
                "Не удалось найти доступный апартамент на этаже 2", name="Warning"
            )
            # Пропускаем тест, если нет доступных апартаментов
            pytest.skip("Нет доступных апартаментов на этаже 2")

    with allure.step("Проверяем финальный URL"):
        final_url = map_page.get_current_url()
        allure.attach(f"Финальный URL: {final_url}", name="Final URL")

        # Проверяем, что мы на странице апартамента
        assert (
            "/apartment/" in final_url or "/unit/" in final_url
        ), f"Не на странице апартамента. URL: {final_url}"
