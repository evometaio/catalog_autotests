import allure
import pytest


@allure.feature("Qube - Проект Cubix")
@allure.story("Explore Amenities")
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.ui
@pytest.mark.parametrize("route_type", ["map", "agent", "client"])
def test_cubix_explore_amenities(cubix_page, route_type):
    """Тест Explore Amenities для проекта Cubix на всех роутах."""
    with allure.step(f"Открываем страницу {route_type}"):
        cubix_page.open(route_type=route_type)

    with allure.step("Кликаем на проект Cubix"):
        cubix_page.map.navigate_to_project("cubix")

    with allure.step("Проверяем наличие кнопки Explore Amenities"):
        cubix_page.browser.expect_visible(
            cubix_page.project_locators.EXPLORE_AMENITIES_BUTTON
        )

    with allure.step("Кликаем на кнопку Explore Amenities"):
        cubix_page.amenities.click_explore_button()

    with allure.step("Проверяем отображение модального окна amenities"):
        cubix_page.amenities.verify_modal_displayed()

    with allure.step("Проверяем наличие заголовка модального окна"):
        cubix_page.amenities.verify_modal_title()

    with allure.step("Проверяем наличие кнопки закрытия модального окна"):
        cubix_page.amenities.verify_modal_close_button()

    with allure.step("Проверяем отображение слайдера в модалке"):
        cubix_page.amenities.verify_slider_displayed()

    with allure.step("Проверяем наличие изображений в слайдере"):
        image_count = cubix_page.amenities.verify_slider_images()
        allure.attach(
            f"Количество изображений в слайдере: {image_count}", name="Image Count"
        )

    with allure.step("Проверяем наличие индикаторов слайдера"):
        indicator_count = cubix_page.amenities.verify_slider_indicators()
        allure.attach(
            f"Количество индикаторов: {indicator_count}", name="Indicator Count"
        )

    with allure.step("Тестируем навигацию по слайдеру - кликаем на индикатор 3"):
        cubix_page.amenities.click_indicator(2)  # Индекс 2 = третий слайд
        # Ждем изменения слайда
        cubix_page.page.wait_for_selector(
            f"{cubix_page.project_locators.AMENITIES_SLIDER_INDICATORS}:nth-child(3)[class*='active']",
            timeout=2000,
        )

    with allure.step("Тестируем навигацию по слайдеру - кликаем на индикатор 4"):
        cubix_page.amenities.click_indicator(3)  # Индекс 3 = четвертый слайд
        # Ждем изменения слайда
        cubix_page.page.wait_for_selector(
            f"{cubix_page.project_locators.AMENITIES_SLIDER_INDICATORS}:nth-child(4)[class*='active']",
            timeout=2000,
        )

    with allure.step("Закрываем модальное окно amenities"):
        cubix_page.amenities.close_modal()

    with allure.step("Проверяем, что модальное окно закрылось"):
        cubix_page.amenities.verify_modal_closed()
