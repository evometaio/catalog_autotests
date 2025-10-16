import allure
import pytest

from pages.page_factory import PageFactory


@allure.feature("Qube - Все проекты")
@allure.story("Explore Amenities - Параметризованный тест")
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.ui
@pytest.mark.parametrize(
    "project_name",
    [
        pytest.param("arisha", marks=pytest.mark.flaky(reruns=2, reruns_delay=2)),
        # "elire",  # Elire имеет другую структуру amenities с множественными заголовками, используйте test_elire_explore_amenities.py
        "cubix",
    ],
)
def test_all_qube_projects_explore_amenities(page, project_name):
    """
    Единый тест Explore Amenities для всех Qube проектов.

    Использует PageFactory для динамического создания нужной страницы проекта.
    Каждый проект имеет свою реализацию доступа к amenities (инкапсулирована в классе),
    но проверки одинаковые.
    """
    # Динамически создаем нужную страницу проекта
    project_page = PageFactory.get_page_by_project(page, project_name)

    with allure.step(f"Открываем карту для проекта {project_name.upper()}"):
        project_page.open(route_type="map")

    with allure.step(f"Переходим к проекту {project_name.upper()}"):
        project_page.map.navigate_to_project(project_name)

    # Каждый проект сам знает как открыть amenities
    # Arisha: click_all_units_button() → amenities.click_explore_button()
    # Elire: click_services_amenities_button()
    # Cubix: amenities.click_explore_button()
    with allure.step(f"Открываем Amenities (специфично для {project_name})"):
        if project_name == "arisha":
            project_page.click_all_units_button()
            project_page.browser.expect_visible(
                project_page.project_locators.EXPLORE_AMENITIES_BUTTON
            )
            project_page.amenities.click_explore_button()
        elif project_name == "elire":
            project_page.click_services_amenities_button()
        else:  # cubix
            project_page.browser.expect_visible(
                project_page.project_locators.EXPLORE_AMENITIES_BUTTON
            )
            project_page.amenities.click_explore_button()

    # Дальше все проверки одинаковые для всех проектов!
    with allure.step("Проверяем отображение модального окна amenities"):
        project_page.amenities.verify_modal_displayed()

    with allure.step("Проверяем наличие заголовка модального окна"):
        project_page.amenities.verify_modal_title()

    with allure.step("Проверяем наличие кнопки закрытия модального окна"):
        project_page.amenities.verify_modal_close_button()

    with allure.step("Проверяем отображение слайдера в модалке"):
        project_page.amenities.verify_slider_displayed()

    with allure.step("Проверяем наличие изображений в слайдере"):
        image_count = project_page.amenities.verify_slider_images()
        allure.attach(
            f"Количество изображений в слайдере: {image_count}", name="Image Count"
        )

    with allure.step("Проверяем наличие индикаторов слайдера"):
        indicator_count = project_page.amenities.verify_slider_indicators()
        allure.attach(
            f"Количество индикаторов: {indicator_count}", name="Indicator Count"
        )

    with allure.step("Тестируем навигацию по слайдеру"):
        # Проверяем 2-3 индикатора
        if indicator_count > 1:
            project_page.amenities.click_indicator(1)
            project_page.page.wait_for_timeout(1000)

        if indicator_count > 2:
            project_page.amenities.click_indicator(2)
            project_page.page.wait_for_timeout(1000)

    with allure.step("Закрываем модальное окно amenities"):
        project_page.amenities.close_modal()

    with allure.step("Проверяем, что модальное окно закрылось"):
        project_page.amenities.verify_modal_closed()
