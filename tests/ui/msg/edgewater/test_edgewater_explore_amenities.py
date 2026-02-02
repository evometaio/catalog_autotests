import allure
import pytest


@allure.feature("MSG - Проект Edgewater")
@allure.story("Explore Amenities")
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.ui
def test_edgewater_explore_amenities(edgewater_page):
    """Тест Explore Amenities для проекта Edgewater."""
    with allure.step("Открываем карту MSG"):
        edgewater_page.open(route_type="map")

    with allure.step("Кликаем на проект Edgewater"):
        edgewater_page.map.navigate_to_project("edgewater")

    with allure.step("Кликаем на кнопку All Units для перехода на catalog2d"):
        edgewater_page.browser.expect_visible(
            edgewater_page.project_locators.ALL_UNITS_BUTTON
        )
        edgewater_page.browser.click(edgewater_page.project_locators.ALL_UNITS_BUTTON)
        edgewater_page.page.wait_for_url("**/catalog_2d", timeout=10000)

    with allure.step("Проверяем наличие кнопки Explore Amenities"):
        edgewater_page.browser.expect_visible(
            edgewater_page.project_locators.EXPLORE_AMENITIES_BUTTON
        )

    with allure.step("Кликаем на кнопку Explore Amenities"):
        edgewater_page.amenities.click_explore_button()

    with allure.step("Проверяем отображение модального окна amenities"):
        edgewater_page.amenities.verify_modal_displayed()

    with allure.step("Проверяем наличие заголовка модального окна"):
        edgewater_page.amenities.verify_modal_title()

    with allure.step("Проверяем наличие кнопки закрытия модального окна"):
        edgewater_page.amenities.verify_modal_close_button()

    with allure.step("Проверяем отображение слайдера в модалке"):
        edgewater_page.amenities.verify_slider_displayed()

    with allure.step("Проверяем наличие изображений в слайдере"):
        image_count = edgewater_page.amenities.verify_slider_images()
        allure.attach(
            f"Количество изображений в слайдере: {image_count}", name="Image Count"
        )

    with allure.step("Проверяем наличие индикаторов слайдера"):
        indicator_count = edgewater_page.amenities.verify_slider_indicators()
        allure.attach(
            f"Количество индикаторов: {indicator_count}", name="Indicator Count"
        )

    with allure.step("Тестируем навигацию по слайдеру - кликаем на индикатор 2"):
        edgewater_page.amenities.click_indicator(1)  # Индекс 1 = второй слайд
        # Ждем изменения слайда
        edgewater_page.page.wait_for_selector(
            f"{edgewater_page.project_locators.AMENITIES_SLIDER_INDICATORS}:nth-child(2)[class*='active']",
            timeout=2000,
        )

    with allure.step("Тестируем навигацию по слайдеру - кликаем на индикатор 3"):
        edgewater_page.amenities.click_indicator(2)  # Индекс 2 = третий слайд
        # Ждем изменения слайда
        edgewater_page.page.wait_for_selector(
            f"{edgewater_page.project_locators.AMENITIES_SLIDER_INDICATORS}:nth-child(3)[class*='active']",
            timeout=2000,
        )

    with allure.step("Закрываем модальное окно amenities"):
        edgewater_page.amenities.close_modal()

    with allure.step("Проверяем, что модальное окно закрылось"):
        edgewater_page.amenities.verify_modal_closed()
