import allure
import pytest


@allure.feature("Wellcube - Проект Tranquil")
@allure.story("Explore Amenities")
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.ui
def test_tranquil_explore_amenities(tranquil_page):
    """Тест Explore Amenities для проекта Tranquil."""
    with allure.step("Открываем карту Wellcube"):
        tranquil_page.open(route_type="map")

    with allure.step("Кликаем на проект Tranquil"):
        tranquil_page.map.navigate_to_project("tranquil")

    with allure.step("Проверяем наличие кнопки Explore Amenities"):
        tranquil_page.browser.expect_visible(
            tranquil_page.project_locators.EXPLORE_AMENITIES_BUTTON
        )

    with allure.step("Кликаем на кнопку Explore Amenities"):
        tranquil_page.amenities.click_explore_button()

    with allure.step("Проверяем отображение модального окна amenities"):
        tranquil_page.amenities.verify_modal_displayed()

    with allure.step("Проверяем наличие заголовка модального окна"):
        tranquil_page.amenities.verify_modal_title()

    with allure.step("Проверяем наличие кнопки закрытия модального окна"):
        tranquil_page.amenities.verify_modal_close_button()

    with allure.step("Проверяем отображение слайдера в модалке"):
        tranquil_page.amenities.verify_slider_displayed()

    with allure.step("Проверяем наличие изображений в слайдере"):
        image_count = tranquil_page.amenities.verify_slider_images()
        allure.attach(
            f"Количество изображений в слайдере: {image_count}", name="Image Count"
        )

    with allure.step("Проверяем наличие индикаторов слайдера"):
        indicator_count = tranquil_page.amenities.verify_slider_indicators()
        allure.attach(
            f"Количество индикаторов: {indicator_count}", name="Indicator Count"
        )

    with allure.step("Тестируем навигацию по слайдеру - кликаем на индикатор 2"):
        tranquil_page.amenities.click_indicator(1)  # Индекс 1 = второй слайд
        # Ждем изменения слайда
        tranquil_page.page.wait_for_selector(
            f"{tranquil_page.project_locators.AMENITIES_SLIDER_INDICATORS}:nth-child(2)[class*='active']",
            timeout=2000,
        )

    with allure.step("Тестируем навигацию по слайдеру - кликаем на индикатор 3"):
        tranquil_page.amenities.click_indicator(2)  # Индекс 2 = третий слайд
        # Ждем изменения слайда
        tranquil_page.page.wait_for_selector(
            f"{tranquil_page.project_locators.AMENITIES_SLIDER_INDICATORS}:nth-child(3)[class*='active']",
            timeout=2000,
        )

    with allure.step("Закрываем модальное окно amenities"):
        tranquil_page.amenities.close_modal()

    with allure.step("Проверяем, что модальное окно закрылось"):
        tranquil_page.amenities.verify_modal_closed()
