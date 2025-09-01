import allure
import pytest


@allure.feature("Qube - Карта, навигация и базовые роуты")
@pytest.mark.ui
class TestQubeMapProjects:
    """Все тесты для проектов Qube: карта, навигация и базовые роуты."""

    @allure.story("Загрузка карты /map")
    @pytest.mark.smoke
    @allure.severity(allure.severity_level.CRITICAL)
    def test_map_page_loads(self, qube_map_page):
        """Тест загрузки страницы карты."""
        with allure.step("Открываем страницу карты"):
            qube_map_page.open_map_page()

        with allure.step("Проверяем, что карта загружена"):
            qube_map_page.check_map_loaded()

    @allure.story("Навигация по всем проектам QUBE")
    @pytest.mark.regression
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("project_name", ["elire", "arisha", "cubix"])
    def test_project_navigation_on_map(self, qube_map_page, project_name):
        """Тест навигации по проектам."""
        with allure.step(f"Открываем страницу карты"):
            qube_map_page.open_map_page()

        with allure.step(f"Кликаем по проекту {project_name.upper()}"):
            qube_map_page.click_project(project_name)

        with allure.step(f"Проверяем информацию о проекте {project_name.upper()}"):
            qube_map_page.check_project_info_visible(project_name)

    @allure.story("Полный цикл навигации по проектам QUBE")
    @pytest.mark.regression
    @pytest.mark.smoke
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize("project_name", ["elire", "arisha", "cubix"])
    def test_full_navigation_cycle_on_map(self, qube_map_page, project_name):
        """Тест полного цикла навигации: карта -> проект -> карта."""
        with allure.step(f"Открываем страницу карты {project_name}"):
            qube_map_page.open_map_page()
            qube_map_page.check_map_loaded()
            qube_map_page.check_project_info_visible(project_name)

        with allure.step(f"Тестируем навигацию для проекта {project_name.upper()}"):
            # Открываем проект
            qube_map_page.open_project_page(project_name)
            qube_map_page.check_project_page_loaded(project_name)

            # Возвращаемся на карту
            qube_map_page.return_to_map_from_project()
            qube_map_page.verify_returned_to_map()