import allure
import pytest


@allure.feature("Abra - Проект Willows Residences")
@allure.story("Explore Amenities")
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.ui
def test_willows_residences_explore_amenities(willows_residences_page):
    """Тест Explore Amenities для проекта Willows Residences."""
    with allure.step("Открываем карту Abra"):
        willows_residences_page.open(route_type="map")

    with allure.step("Кликаем на проект Willows Residences"):
        willows_residences_page.map.navigate_to_project("willows_residences")

    with allure.step("Проверяем наличие кнопки Explore Amenities"):
        willows_residences_page.browser.expect_visible(
            willows_residences_page.project_locators.EXPLORE_AMENITIES_BUTTON
        )

    with allure.step("Кликаем на кнопку Explore Amenities"):
        willows_residences_page.amenities.click_explore_button()

    with allure.step("Проверяем отображение модального окна amenities"):
        willows_residences_page.amenities.verify_modal_displayed()

    with allure.step("Проверяем наличие заголовка модального окна"):
        willows_residences_page.amenities.verify_modal_title()

    with allure.step("Проверяем наличие кнопки закрытия модального окна"):
        willows_residences_page.amenities.verify_modal_close_button()

    with allure.step("Проверяем отображение слайдера в модалке"):
        willows_residences_page.amenities.verify_slider_displayed()

    with allure.step("Проверяем наличие изображений в слайдере"):
        image_count = willows_residences_page.amenities.verify_slider_images()
        allure.attach(
            f"Количество изображений в слайдере: {image_count}", name="Image Count"
        )

    with allure.step("Проверяем наличие индикаторов слайдера"):
        indicator_count = willows_residences_page.amenities.verify_slider_indicators()
        allure.attach(
            f"Количество индикаторов: {indicator_count}", name="Indicator Count"
        )

    with allure.step("Тестируем навигацию по слайдеру"):
        # Кликаем на индикатор 2, если он есть
        if indicator_count >= 2:
            willows_residences_page.amenities.click_indicator(
                1
            )  # Индекс 1 = второй слайд
            # Ждем изменения слайда
            willows_residences_page.page.wait_for_selector(
                f"{willows_residences_page.project_locators.AMENITIES_SLIDER_INDICATORS}:nth-child(2)[class*='active']",
                timeout=2000,
            )
            allure.attach("Кликнули на индикатор 2", name="Slider Navigation")

        # Кликаем на индикатор 3, если он есть
        if indicator_count >= 3:
            willows_residences_page.amenities.click_indicator(
                2
            )  # Индекс 2 = третий слайд
            # Ждем изменения слайда
            willows_residences_page.page.wait_for_selector(
                f"{willows_residences_page.project_locators.AMENITIES_SLIDER_INDICATORS}:nth-child(3)[class*='active']",
                timeout=2000,
            )
            allure.attach("Кликнули на индикатор 3", name="Slider Navigation")
        else:
            allure.attach(
                f"Индикатор 3 отсутствует (всего индикаторов: {indicator_count})",
                name="Slider Navigation",
            )

    with allure.step("Закрываем модальное окно amenities"):
        willows_residences_page.amenities.close_modal()

    with allure.step("Проверяем, что модальное окно закрылось"):
        willows_residences_page.amenities.verify_modal_closed()
