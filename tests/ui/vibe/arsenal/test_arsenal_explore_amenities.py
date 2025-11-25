import allure
import pytest


@allure.feature("Vibe - Проект Arsenal")
@allure.story("Explore Amenities")
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.ui
def test_arsenal_explore_amenities(arsenal_page):
    """Тест Explore Amenities для проекта Arsenal (без routes, только map)."""
    with allure.step("Открываем страницу map"):
        arsenal_page.open(route_type="map")

    with allure.step("Кликаем на кнопку All units для перехода на catalog2d"):
        arsenal_page.click_all_units_button()

    with allure.step("Проверяем наличие кнопки Explore Amenities"):
        arsenal_page.browser.expect_visible(
            arsenal_page.project_locators.EXPLORE_AMENITIES_BUTTON
        )

    with allure.step("Кликаем на кнопку Explore Amenities"):
        arsenal_page.amenities.click_explore_button()

    with allure.step("Проверяем отображение модального окна amenities"):
        arsenal_page.amenities.verify_modal_displayed()

    with allure.step("Проверяем наличие заголовка модального окна"):
        arsenal_page.amenities.verify_modal_title()

    with allure.step("Проверяем наличие кнопки закрытия модального окна"):
        arsenal_page.amenities.verify_modal_close_button()

    with allure.step("Проверяем отображение слайдера в модалке"):
        arsenal_page.amenities.verify_slider_displayed()

    with allure.step("Проверяем наличие изображений в слайдере"):
        image_count = arsenal_page.amenities.verify_slider_images()
        allure.attach(
            f"Количество изображений в слайдере: {image_count}", name="Image Count"
        )

    with allure.step("Проверяем наличие индикаторов слайдера"):
        indicator_count = arsenal_page.amenities.verify_slider_indicators()
        allure.attach(
            f"Количество индикаторов: {indicator_count}", name="Indicator Count"
        )

    with allure.step("Тестируем навигацию по слайдеру - кликаем на индикатор 3"):
        arsenal_page.amenities.click_indicator(2)  # Индекс 2 = третий слайд
        # Ждем изменения слайда
        arsenal_page.page.wait_for_selector(
            f"{arsenal_page.project_locators.AMENITIES_SLIDER_INDICATORS}:nth-child(3)[class*='active']",
            timeout=2000,
        )

    with allure.step("Тестируем навигацию по слайдеру - кликаем на индикатор 4"):
        arsenal_page.amenities.click_indicator(3)  # Индекс 3 = четвертый слайд
        # Ждем изменения слайда
        arsenal_page.page.wait_for_selector(
            f"{arsenal_page.project_locators.AMENITIES_SLIDER_INDICATORS}:nth-child(4)[class*='active']",
            timeout=2000,
        )

    with allure.step("Закрываем модальное окно amenities"):
        arsenal_page.amenities.close_modal()

    with allure.step("Проверяем, что модальное окно закрылось"):
        arsenal_page.amenities.verify_modal_closed()
