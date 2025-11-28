import allure
import pytest


@allure.feature("LSR - Проект MARK (mobile)")
@allure.story("Навигация по зданиям, этажам и апартаментам")
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.mobile
@pytest.mark.iphone
@pytest.mark.flaky(reruns=2, reruns_delay=2)
def test_mark_mobile_building_floor_apartment_navigation(mobile_page):
    """Тест навигации по зданиям, этажам и апартаментам проекта MARK на мобильном устройстве."""

    with allure.step("Открываем страницу MARK на мобильном"):
        # Для MARK нет map роута, открываем напрямую страницу проекта
        mobile_page.page.goto(mobile_page.base_url)
        mobile_page.wait_for_page_load()

    with allure.step("Открываем мобильное меню"):
        mobile_page.mobile_navigation.open_mobile_menu()

    with allure.step("Навигация по зданию 1, этажу 6"):
        mobile_page.mobile_navigation.close_zoom_modal()

        # Кликаем на "Корпус" в мобильном меню
        mobile_page.mobile_navigation.click_mark_building_menu()

        # Кликаем на корпус 1
        building_clicked = mobile_page.mobile_navigation.click_mark_building_item(
            building_number=1
        )
        mobile_page.assertions.assert_that(
            building_clicked, "Не удалось кликнуть по корпусу 1"
        )
        mobile_page.assertions.assert_url_contains(
            "/building/mark-k1", "Не перешли на страницу здания 1"
        )

        # Ждем появления этажей внизу страницы
        mobile_page.browser.wait_for_timeout(2000)

        # Кликаем на этаж 6 внизу страницы
        floor_clicked = mobile_page.mobile_navigation.click_mark_floor_item(
            floor_number=6
        )
        mobile_page.assertions.assert_that(
            floor_clicked, "Не удалось кликнуть по этажу 6"
        )

        # Кликаем на кнопку "Посмотреть этаж 6"
        view_floor_clicked = mobile_page.mobile_navigation.click_mark_view_floor_button(
            floor_number=6
        )
        mobile_page.assertions.assert_that(
            view_floor_clicked, "Не удалось кликнуть по кнопке 'Посмотреть этаж 6'"
        )

        # Ждем появления апартаментов внизу страницы
        mobile_page.browser.wait_for_timeout(2000)

        # Выбираем первый доступный апартамент из списка внизу страницы
        apartment_number = mobile_page.mobile_navigation.click_mark_apartment_item()
        mobile_page.assertions.assert_that(
            apartment_number, "Не удалось выбрать апартамент"
        )

        # Кликаем на кнопку "Посмотреть квартиру {номер}"
        view_apartment_clicked = (
            mobile_page.mobile_navigation.click_mark_view_apartment_button(
                apartment_number
            )
        )
        mobile_page.assertions.assert_that(
            view_apartment_clicked,
            f"Не удалось кликнуть по кнопке 'Посмотреть квартиру {apartment_number}'",
        )

    with allure.step("Кликаем на кнопку 'Посмотреть 3D Тур'"):
        view_3d_clicked = mobile_page.mobile_navigation.click_mark_view_3d_button()
        mobile_page.assertions.assert_that(
            view_3d_clicked, "Не удалось кликнуть по кнопке 'Посмотреть 3D Тур'"
        )

    with allure.step("Проверяем адаптивность на мобильном устройстве"):
        mobile_page.check_mobile_viewport_adaptation()
