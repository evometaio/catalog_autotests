import allure
import pytest


@allure.feature("Qube - Проект Arisha (Мобильная)")
@allure.story("Навигация по зданиям Arisha")
@pytest.mark.mobile
@pytest.mark.iphone
class TestArishaMobileBuildingNavigation:
    """Тесты навигации по зданиям, этажам и квартирам для мобильных устройств."""

    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.mobile
    @pytest.mark.regression
    def test_arisha_mobile_building_floor_apartment_navigation(self, mobile_page):
        """Тест полной навигации по зданию, этажу и квартире на мобильном устройстве."""

        with allure.step("Переход на страницу /area Arisha"):
            # Открываем карту
            mobile_page.open()

            # Кликаем на проект Arisha
            mobile_page.click_mobile_project_on_map("arisha")
            mobile_page.wait_for_mobile_project_modal()
            mobile_page.click_mobile_explore_project_button("arisha")

            # Проверяем что попали на страницу area
            current_url = mobile_page.page.url
            assert (
                "/area" in current_url
            ), f"Ожидался URL с /area, получен: {current_url}"

        with allure.step("Навигация по зданию 1, этажу 1"):
            mobile_page.close_zoom_modal()

            # Кликаем на здание
            building_clicked = mobile_page.click_building("1")
            assert building_clicked, "Не удалось кликнуть по зданию 1"

            # Кликаем на кнопку "View 1"
            view_clicked = mobile_page.click_view_building_button()
            assert view_clicked, "Не удалось кликнуть по кнопке View 1"

            # Ждем обновления UI после клика "View 1" (как в отладочном скрипте)
            print("🔧 Ждем обновления UI...")
            mobile_page.wait_for_timeout(3000)

            # Кликаем на этаж
            floor_clicked = mobile_page.click_floor("1")
            assert floor_clicked, "Не удалось кликнуть по этажу 1"

            # Кликаем на кнопку "View Floor 1"
            floor_view_clicked = mobile_page.click_view_floor_button()
            assert floor_view_clicked, "Не удалось кликнуть по кнопке View Floor 1"

            # Ждем перехода в floor plan (как в отладочном скрипте)
            mobile_page.wait_for_timeout(3000)

            # Проверяем, что мы попали в floor plan
            current_url = mobile_page.page.url

            if "/floor/" in current_url:
                print("✅ Успешно попали в floor plan!")
            else:
                # Попробуем еще раз подождать
                mobile_page.wait_for_timeout(2000)

            # Кликаем на квартиру (как в отладочном скрипте)
            mobile_page.click_apartment_on_plan()

            # Ждем появления модального окна с кнопками
            mobile_page.wait_for_timeout(2000)

            # Кликаем на "View Apartment"
            mobile_page.click_view_apartment_button()

            # Ждем загрузки страницы квартиры
            mobile_page.wait_for_timeout(3000)

            # Кликаем на "View in 3D"
            mobile_page.click_view_3d_button()

        with allure.step("Проверка финального URL"):
            final_url = mobile_page.page.url

            # Проверяем, что мы попали в 3D квартиры (URL должен содержать /apartment/)
            assert (
                "/apartment/" in final_url
            ), f"Ожидался URL с /apartment/, получен: {final_url}"

        with allure.step("Проверяем адаптивность на мобильном устройстве"):
            mobile_page.check_mobile_viewport_adaptation()
