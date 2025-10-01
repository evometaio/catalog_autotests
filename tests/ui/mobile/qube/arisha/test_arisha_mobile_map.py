import allure
import pytest


@allure.feature("Qube - Проект Arisha (Mobile)")
@allure.story("Мобильная навигация по карте")
@pytest.mark.mobile
@pytest.mark.ui
@pytest.mark.smoke
class TestArishaMobileMap:
    """Мобильные тесты для проекта Arisha."""

    @pytest.mark.mobile_device("iPhone 13 Pro")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_arisha_mobile_map_loads(self, mobile_map_page):
        """Тест загрузки мобильной карты проекта Arisha."""
        with allure.step("Открываем мобильную страницу карты"):
            mobile_map_page.open(route_type="map")

        with allure.step("Проверяем, что карта загружена на мобильном устройстве"):
            mobile_map_page.check_map_loaded()

        with allure.step("Проверяем мобильные элементы интерфейса"):
            # Здесь будут мобильные локаторы
            pass  # TODO: Добавить проверку мобильных элементов

    @pytest.mark.mobile_device("iPhone 13 Pro")
    @pytest.mark.regression
    @allure.severity(allure.severity_level.NORMAL)
    def test_arisha_mobile_project_navigation(self, mobile_map_page):
        """Тест мобильной навигации по проекту Arisha."""
        with allure.step("Открываем мобильную страницу карты"):
            mobile_map_page.open(route_type="map")

        with allure.step("Кликаем по проекту Arisha на мобильном устройстве"):
            mobile_map_page.click_project("arisha")

        with allure.step("Проверяем информацию о проекте на мобильном"):
            mobile_map_page.check_project_info_visible("arisha")

    @pytest.mark.mobile_device("Pixel 5")
    @pytest.mark.regression
    @allure.severity(allure.severity_level.NORMAL)
    def test_arisha_android_navigation(self, mobile_map_page):
        """Тест навигации по проекту Arisha на Android устройстве."""
        with allure.step("Открываем мобильную страницу карты"):
            mobile_map_page.open(route_type="map")

        with allure.step("Кликаем по проекту Arisha на Android"):
            mobile_map_page.click_project("arisha")

        with allure.step("Проверяем информацию о проекте на Android"):
            mobile_map_page.check_project_info_visible("arisha")

    @pytest.mark.mobile_device("iPad")
    @pytest.mark.regression
    @allure.severity(allure.severity_level.NORMAL)
    def test_arisha_tablet_navigation(self, mobile_map_page):
        """Тест навигации по проекту Arisha на планшете."""
        with allure.step("Открываем страницу карты на планшете"):
            mobile_map_page.open(route_type="map")

        with allure.step("Кликаем по проекту Arisha на планшете"):
            mobile_map_page.click_project("arisha")

        with allure.step("Проверяем информацию о проекте на планшете"):
            mobile_map_page.check_project_info_visible("arisha")


@allure.feature("Qube - Проект Arisha (Mobile)")
@allure.story("Мобильная навигация по апартаментам")
@pytest.mark.mobile
@pytest.mark.ui
@pytest.mark.regression
class TestArishaMobileApartmentNavigation:
    """Мобильные тесты навигации по апартаментам Arisha."""

    @pytest.mark.mobile_device("iPhone 13 Pro")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_arisha_mobile_building_floor_navigation(self, mobile_map_page):
        """Тест мобильной навигации по зданиям и этажам."""
        with allure.step("Открываем мобильную страницу карты"):
            mobile_map_page.open(route_type="map")

        with allure.step("Переходим к проекту Arisha"):
            mobile_map_page.click_project_on_map("arisha")

        with allure.step("Выбираем здание 1 на мобильном"):
            mobile_map_page.click(mobile_map_page.project_locators.BUILDING_NAV_BUTTON)
            mobile_map_page.click(mobile_map_page.project_locators.BUILDING_1_BUTTON)

        with allure.step("Выбираем этаж 1 на мобильном"):
            mobile_map_page.click(mobile_map_page.project_locators.FLOOR_NAV_BUTTON)
            mobile_map_page.click(mobile_map_page.project_locators.FLOOR_1_BUTTON)

        with allure.step("Проверяем загрузку плана этажа на мобильном"):
            mobile_map_page.page.wait_for_selector(
                mobile_map_page.project_locators.FLOOR_PLAN_APARTMENTS, timeout=10000
            )

