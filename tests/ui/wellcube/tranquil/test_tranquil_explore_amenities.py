import allure
import pytest


@allure.feature("Wellcube - Проект Tranquil")
@allure.story("Explore Amenities")
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.ui
def test_tranquil_explore_amenities(wellcube_page):
    """Тест Explore Amenities для проекта Tranquil."""
    with allure.step("Открываем карту Wellcube"):
        wellcube_page.open(route_type="map")

    with allure.step("Кликаем на проект Tranquil"):
        wellcube_page.click_project_on_map("tranquil")

    with allure.step("Проверяем наличие кнопки Explore Amenities"):
        wellcube_page.expect_visible(wellcube_page.locators.EXPLORE_AMENITIES_BUTTON)

    with allure.step("Кликаем на кнопку Explore Amenities"):
        wellcube_page.click_explore_amenities_button()

    with allure.step("Проверяем отображение модального окна amenities"):
        wellcube_page.verify_amenities_modal_displayed()

    with allure.step("Проверяем наличие заголовка модального окна"):
        wellcube_page.verify_amenities_modal_title()

    with allure.step("Проверяем наличие кнопки закрытия модального окна"):
        wellcube_page.verify_amenities_modal_close_button()

    with allure.step("Проверяем отображение слайдера в модалке"):
        wellcube_page.verify_amenities_slider_displayed()

    with allure.step("Проверяем наличие изображений в слайдере"):
        image_count = wellcube_page.verify_amenities_slider_images()
        allure.attach(
            f"Количество изображений в слайдере: {image_count}", name="Image Count"
        )

    with allure.step("Проверяем наличие индикаторов слайдера"):
        indicator_count = wellcube_page.verify_amenities_slider_indicators()
        allure.attach(
            f"Количество индикаторов: {indicator_count}", name="Indicator Count"
        )

    with allure.step("Тестируем навигацию по слайдеру - кликаем на индикатор 2"):
        wellcube_page.click_amenities_slider_indicator(1)  # Индекс 1 = второй слайд
        # Ждем изменения слайда - проверяем что активный индикатор изменился
        wellcube_page.page.wait_for_selector(
            f"{locators.get("AMENITIES_SLIDER_INDICATORS")}:nth-child(2)[class*='active']",
            timeout=2000,
        )

    with allure.step("Тестируем навигацию по слайдеру - кликаем на индикатор 3"):
        wellcube_page.click_amenities_slider_indicator(2)  # Индекс 2 = третий слайд
        # Ждем изменения слайда - проверяем что активный индикатор изменился
        wellcube_page.page.wait_for_selector(
            f"{locators.get("AMENITIES_SLIDER_INDICATORS")}:nth-child(3)[class*='active']",
            timeout=2000,
        )

    with allure.step("Закрываем модальное окно amenities"):
        wellcube_page.close_amenities_modal()

    with allure.step("Проверяем, что модальное окно закрылось"):
        wellcube_page.verify_amenities_modal_closed()
