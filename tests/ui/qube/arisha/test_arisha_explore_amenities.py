import os

import allure
import pytest


@allure.feature("Qube - Проект Arisha")
@allure.story("Explore Amenities")
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.ui
@pytest.mark.skipif(
    os.getenv("TEST_ENVIRONMENT", "dev") == "prod",
    reason="тест временно отключен на PROD",
)
def test_arisha_explore_amenities(map_page):
    """Тест Explore Amenities для проекта Arisha."""
    with allure.step("Открываем карту"):
        map_page.open(route_type="map")

    with allure.step("Кликаем на проект Arisha"):
        map_page.click_project_on_map("arisha")

    with allure.step("Кликаем на кнопку All units для перехода на catalog2d"):
        map_page.click_on_all_units_button()

    with allure.step("Проверяем наличие кнопки Explore Amenities"):
        map_page.expect_visible(map_page.project_locators.EXPLORE_AMENITIES_BUTTON)

    with allure.step("Кликаем на кнопку Explore Amenities"):
        map_page.click_explore_amenities_button()

    with allure.step("Проверяем отображение модального окна amenities"):
        map_page.verify_amenities_modal_displayed()

    with allure.step("Проверяем наличие заголовка модального окна"):
        map_page.verify_amenities_modal_title()

    with allure.step("Проверяем наличие кнопки закрытия модального окна"):
        map_page.verify_amenities_modal_close_button()

    with allure.step("Проверяем отображение слайдера в модалке"):
        map_page.verify_amenities_slider_displayed()

    with allure.step("Проверяем наличие изображений в слайдере"):
        image_count = map_page.verify_amenities_slider_images()
        allure.attach(
            f"Количество изображений в слайдере: {image_count}", name="Image Count"
        )

    with allure.step("Проверяем наличие индикаторов слайдера"):
        indicator_count = map_page.verify_amenities_slider_indicators()
        allure.attach(
            f"Количество индикаторов: {indicator_count}", name="Indicator Count"
        )

    with allure.step("Тестируем навигацию по слайдеру - кликаем на индикатор 2"):
        map_page.click_amenities_slider_indicator(1)  # Индекс 1 = второй слайд
        map_page.wait_for_timeout(1000)  # Ждем анимации

    with allure.step("Тестируем навигацию по слайдеру - кликаем на индикатор 5"):
        map_page.click_amenities_slider_indicator(4)  # Индекс 4 = пятый слайд
        map_page.wait_for_timeout(1000)  # Ждем анимации

    with allure.step("Закрываем модальное окно amenities"):
        map_page.close_amenities_modal()

    with allure.step("Проверяем, что модальное окно закрылось"):
        map_page.verify_amenities_modal_closed()
