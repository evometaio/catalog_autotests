import allure
import pytest


@allure.feature("Qube - Карта, навигация и базовые роуты")
@pytest.mark.ui
class TestQubeMapProjects:
    """Все тесты для проектов Qube: карта, навигация и базовые роуты."""

    @allure.story("Загрузка карты /map")
    @pytest.mark.smoke
    @allure.severity(allure.severity_level.CRITICAL)
    def test_map_page_loads(self, map_page):
        """Тест загрузки страницы карты."""
        with allure.step("Открываем страницу карты"):
            map_page.open(route_type="map")

        with allure.step("Проверяем, что карта загружена"):
            map_page.check_map_loaded()

    @allure.story("Навигация по всем проектам QUBE")
    @pytest.mark.regression
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("project_name", ["elire", "arisha", "cubix"])
    def test_project_navigation_on_map(self, map_page, project_name):
        """Тест навигации по проектам."""
        with allure.step(f"Открываем страницу карты"):
            map_page.open(route_type="map")

        with allure.step(f"Кликаем по проекту {project_name.upper()}"):
            map_page.click_project(project_name)

        with allure.step(f"Проверяем информацию о проекте {project_name.upper()}"):
            map_page.check_project_info_visible(project_name)

    @allure.story("Полный цикл навигации по проектам QUBE")
    @pytest.mark.regression
    @pytest.mark.smoke
    @allure.severity(allure.severity_level.CRITICAL)
    # TODO: Добавить "cubix" после фикса локаторов
    @pytest.mark.parametrize("project_name", ["arisha", "elire"])
    def test_full_navigation_cycle_on_map(self, map_page, project_name):
        """Тест полного цикла навигации: карта -> проект -> карта."""
        with allure.step(f"Открываем страницу карты"):
            map_page.open(route_type="map")
            map_page.check_map_loaded()

        with allure.step(f"Переходим на страницу проекта {project_name}"):
            map_page.click_project_on_map(project_name)
            map_page.check_project_page_loaded(project_name)

        with allure.step(f"Возвращаемся на карту"):
            map_page.return_to_map_from_project_and_verify_returned_to_map()

    @allure.story("Тестовый кастомный POI")
    @pytest.mark.smoke
    @allure.severity(allure.severity_level.CRITICAL)
    def test_arisha_map_poi(self, map_page):
        """Тест кастомного POI на карте"""

        with allure.step("Открываем страницу карты"):
            map_page.open(route_type="map")

        with allure.step("Кликаем на кастомный POI"):
            map_page.click_on_custom_poi()