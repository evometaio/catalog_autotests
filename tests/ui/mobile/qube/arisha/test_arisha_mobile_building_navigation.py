import allure
import pytest


@allure.feature("Qube - Проект Arisha (mobile)")
@allure.story("Навигация по зданиям Arisha")
@pytest.mark.mobile
@pytest.mark.iphone
@pytest.mark.flaky(reruns=2, reruns_delay=2)
class TestArishaMobileBuildingNavigation:
    """Тесты навигации по зданиям, этажам и квартирам для мобильных устройств."""

    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.mobile
    @pytest.mark.regression
    @pytest.mark.parametrize("route_type", ["map", "agent", "client"])
    def test_arisha_mobile_building_floor_apartment_navigation(
        self, mobile_page, route_type
    ):
        """Тест полной навигации по зданию, этажу и квартире на мобильном устройстве на всех роутах."""

        with allure.step(f"Переход на страницу /area Arisha через {route_type}"):
            # Открываем карту
            mobile_page.open(route_type=route_type)

            # Кликаем на проект Arisha
            mobile_page.mobile_map.click_project("arisha")
            mobile_page.mobile_map.wait_for_project_modal()
            mobile_page.mobile_map.click_explore_project("arisha")

            # Проверяем что попали на страницу area
            mobile_page.assertions.assert_url_contains(
                "/area", "Не перешли на страницу /area после клика на проект"
            )

        with allure.step("Навигация по зданию 1, этажу 1"):
            mobile_page.mobile_navigation.close_zoom_modal()

            # Кликаем на здание
            building_clicked = mobile_page.mobile_navigation.click_building("1")
            mobile_page.assertions.assert_that(
                building_clicked, "Не удалось кликнуть по зданию 1"
            )

            # Кликаем на кнопку "View 1"
            view_clicked = mobile_page.mobile_navigation.click_view_building_button()
            mobile_page.assertions.assert_that(
                view_clicked, "Не удалось кликнуть по кнопке View 1"
            )

            # Ждем обновления UI после клика "View 1"
            mobile_page.browser.wait_for_timeout(3000)

            # Кликаем на этаж
            floor_clicked = mobile_page.mobile_navigation.click_floor("1")
            mobile_page.assertions.assert_that(
                floor_clicked, "Не удалось кликнуть по этажу 1"
            )

            # Кликаем на кнопку "View Floor 1"
            floor_view_clicked = mobile_page.mobile_navigation.click_view_floor_button()
            mobile_page.assertions.assert_that(
                floor_view_clicked, "Не удалось кликнуть по кнопке View Floor 1"
            )

            # Ждем перехода в floor plan
            mobile_page.browser.wait_for_timeout(3000)

            # Кликаем на квартиру
            mobile_page.mobile_navigation.click_apartment_on_plan()

            # Ждем появления модального окна с кнопками
            mobile_page.browser.wait_for_timeout(2000)

            # Кликаем на "View Apartment"
            mobile_page.mobile_navigation.click_view_apartment_button()

            # Ждем загрузки страницы квартиры
            mobile_page.browser.wait_for_timeout(3000)

            # Кликаем на "View in 3D"
            mobile_page.click_view_3d_button()

        with allure.step("Проверяем адаптивность на мобильном устройстве"):
            mobile_page.check_mobile_viewport_adaptation()
