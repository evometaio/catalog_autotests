import allure
import pytest


@allure.feature("Страница карты")
@allure.story("Загрузка карты")
@pytest.mark.smoke
@pytest.mark.ui
@allure.severity(allure.severity_level.CRITICAL)
def test_map_page_loads(map_page):
    """Тест загрузки страницы карты."""
    with allure.step("Открываем страницу карты"):
        map_page.open_map_page()

    with allure.step("Проверяем, что карта загружена"):
        map_page.check_map_loaded()


# TODO подумать как реализизовать
@allure.feature("Страница карты")
@allure.story("Все элементы")
@pytest.mark.skip(reason="Флаки тест")
@pytest.mark.regression
@pytest.mark.ui
@allure.severity(allure.severity_level.NORMAL)
def test_map_page_all_elements(map_page):
    """Тест всех основных элементов страницы карты."""
    with allure.step("Открываем страницу карты"):
        map_page.open_map_page()

    with allure.step("Проверяем все основные элементы"):
        map_page.check_all_elements()


@allure.feature("Страница карты")
@allure.story("Проекты на карте")
@pytest.mark.regression
@pytest.mark.ui
@allure.severity(allure.severity_level.NORMAL)
def test_all_projects_visible_on_map(map_page):
    """Тест видимости всех проектов на карте."""
    with allure.step("Открываем страницу карты"):
        map_page.open_map_page()

    with allure.step("Проверяем видимость всех проектов"):
        map_page.check_all_projects_visible()


@allure.feature("Страница карты")
@allure.story("Навигация по проектам")
@pytest.mark.regression
@pytest.mark.ui
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.parametrize("project_name", ["elire", "arisha", "cubix"])
def test_project_navigation_on_map(map_page, project_name):
    """Тест навигации по проектам."""
    with allure.step(f"Открываем страницу карты"):
        map_page.open_map_page()

    with allure.step(f"Кликаем по проекту {project_name.upper()}"):
        map_page.click_project(project_name)

    with allure.step(f"Проверяем информацию о проекте {project_name.upper()}"):
        map_page.check_project_info_visible(project_name)


@allure.feature("Страница карты")
@allure.story("Полный цикл навигации")
@pytest.mark.regression
@pytest.mark.ui
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.parametrize("project_name", ["elire", "arisha", "cubix"])
def test_full_navigation_cycle_on_map(map_page, project_name):
    """Тест полного цикла навигации: карта -> проект -> карта."""
    with allure.step(f"Открываем страницу карты"):
        map_page.open_map_page()

    with allure.step(f"Тестируем навигацию для проекта {project_name.upper()}"):
        # Открываем проект
        map_page.open_project_page(project_name)
        map_page.check_project_page_loaded(project_name)

        # Возвращаемся на карту
        map_page.return_to_map_from_project()
        map_page.verify_returned_to_map()


# TODO подумать как реализизовать
@allure.feature("Страница карты")
@allure.story("Функциональность зума")
@pytest.mark.skip(reason="Флаки тест")
@pytest.mark.regression
@pytest.mark.ui
@allure.severity(allure.severity_level.NORMAL)
def test_map_zoom_functionality(map_page):
    """Тест функциональности зума карты."""
    with allure.step("Открываем страницу карты"):
        map_page.open_map_page()

    with allure.step("Приближаем карту"):
        map_page.zoom_in()

    with allure.step("Отдаляем карту"):
        map_page.zoom_out()


@allure.feature("Страница карты")
@allure.story("Полноэкранный режим")
@pytest.mark.regression
@pytest.mark.ui
@allure.severity(allure.severity_level.MINOR)
def test_fullscreen_mode_on_map(map_page):
    """Тест полноэкранного режима."""
    with allure.step("Открываем страницу карты"):
        map_page.open_map_page()

    with allure.step("Переключаем полноэкранный режим"):
        map_page.toggle_fullscreen()
