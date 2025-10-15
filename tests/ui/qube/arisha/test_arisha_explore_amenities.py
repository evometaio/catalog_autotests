import allure
import pytest


@allure.feature("Qube - Проект Arisha")
@allure.story("Explore Amenities")
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.ui
@pytest.mark.flaky(reruns=2, reruns_delay=4)
def test_arisha_explore_amenities(arisha_page):
    """Тест Explore Amenities для проекта Arisha."""
    with allure.step("Открываем карту"):
        arisha_page.open(route_type="map")

    with allure.step("Кликаем на проект Arisha"):
        arisha_page.map.navigate_to_project("arisha")

    with allure.step("Кликаем на кнопку All units для перехода на catalog2d"):
        arisha_page.click_all_units_button()

    with allure.step("Проверяем наличие кнопки Explore Amenities"):
        arisha_page.browser.expect_visible(arisha_page.project_locators.EXPLORE_AMENITIES_BUTTON)

    with allure.step("Кликаем на кнопку Explore Amenities"):
        arisha_page.amenities.click_explore_button()

    with allure.step("Проверяем отображение модального окна amenities"):
        arisha_page.amenities.verify_modal_displayed()

    with allure.step("Проверяем наличие заголовка модального окна"):
        arisha_page.amenities.verify_modal_title()

    with allure.step("Проверяем наличие кнопки закрытия модального окна"):
        arisha_page.amenities.verify_modal_close_button()

    with allure.step("Проверяем отображение слайдера в модалке"):
        arisha_page.amenities.verify_slider_displayed()

    with allure.step("Проверяем наличие изображений в слайдере"):
        image_count = arisha_page.amenities.verify_slider_images()
        allure.attach(
            f"Количество изображений в слайдере: {image_count}", name="Image Count"
        )

    with allure.step("Проверяем наличие индикаторов слайдера"):
        indicator_count = arisha_page.amenities.verify_slider_indicators()
        allure.attach(
            f"Количество индикаторов: {indicator_count}", name="Indicator Count"
        )

    with allure.step("Тестируем навигацию по слайдеру - кликаем на индикатор 2"):
        arisha_page.amenities.click_indicator(1)  # Индекс 1 = второй слайд
        # Ждем изменения слайда
        arisha_page.page.wait_for_selector(
            f"{arisha_page.project_locators.AMENITIES_SLIDER_INDICATORS}:nth-child(2)[class*='active']",
            timeout=2000,
        )

    with allure.step("Тестируем навигацию по слайдеру - кликаем на индикатор 5"):
        arisha_page.amenities.click_indicator(4)  # Индекс 4 = пятый слайд
        # Ждем изменения слайда
        arisha_page.page.wait_for_selector(
            f"{arisha_page.project_locators.AMENITIES_SLIDER_INDICATORS}:nth-child(5)[class*='active']",
            timeout=2000,
        )

    with allure.step("Закрываем модальное окно amenities"):
        arisha_page.amenities.close_modal()

    with allure.step("Проверяем, что модальное окно закрылось"):
        arisha_page.amenities.verify_modal_closed()
