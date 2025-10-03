"""
Мобильные тесты для навигации по зданиям, этажам и квартирам в проекте Arisha.
Тесты адаптированы для мобильных устройств с использованием специальных локаторов.
"""

import pytest
import allure


@allure.feature("Mobile Navigation")
@allure.story("Arisha Building Navigation")
@pytest.mark.mobile
@pytest.mark.iphone
class TestArishaMobileBuildingNavigation:
    """Тесты навигации по зданиям, этажам и квартирам для мобильных устройств."""

    @allure.story("Arisha Building Navigation - Mobile")
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
            assert "/area" in current_url, f"Ожидался URL с /area, получен: {current_url}"
            
        with allure.step("Закрытие модального окна"):
            mobile_page.close_zoom_modal()
            
        with allure.step("Навигация по зданию 1, этажу 1"):
            navigation_success = mobile_page.navigate_building_floor_apartment(
                building_number="1",
                floor_number="1"
            )
            assert navigation_success, "Навигация не выполнена успешно"
            
        with allure.step("Проверка финального URL"):
            final_url = mobile_page.page.url
            assert "/building/" in final_url, f"Ожидался URL с /building/, получен: {final_url}"
            
        with allure.step("Проверяем адаптивность на мобильном устройстве"):
            mobile_page.check_mobile_viewport_adaptation()