import allure
import pytest


@allure.feature("Vibe - Проект Arsenal (mobile)")
@allure.story("Explore Amenities")
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.mobile
def test_arsenal_mobile_explore_amenities(mobile_page):
    """Тест Explore Amenities для проекта Arsenal на мобильном устройстве."""
    with allure.step("Открываем страницу map"):
        mobile_page.open(route_type="map")

    with allure.step("Переходим на страницу проекта через навигацию"):
        mobile_page.mobile_map.navigate_to_project("arsenal")

    with allure.step("Кликаем на кнопку All units для перехода на catalog2d"):
        all_units_button = mobile_page.page.locator(
            '[data-test-id="nav-desktop-catalog2d-standalone"]'
        )
        all_units_button.wait_for(state="attached", timeout=10000)
        mobile_page.page.evaluate(
            """
            document.querySelector('[data-test-id="nav-desktop-catalog2d-standalone"]').click();
        """
        )
        mobile_page.page.wait_for_url("**/catalog_2d", timeout=10000)

    with allure.step("Кликаем на кнопку Explore Amenities"):
        explore_button = mobile_page.page.locator(
            '(//button[@data-test-id="project-info-window-explore-amenities"])[1]'
        )
        explore_button.wait_for(state="visible", timeout=10000)
        explore_button.click()

    with allure.step("Проверяем отображение модального окна amenities"):
        mobile_page.amenities.verify_modal_displayed()

    with allure.step("Проверяем наличие заголовка модального окна"):
        mobile_page.amenities.verify_modal_title()

    with allure.step("Проверяем наличие кнопки закрытия модального окна"):
        mobile_page.amenities.verify_modal_close_button()

    with allure.step("Проверяем отображение слайдера в модалке"):
        mobile_page.amenities.verify_slider_displayed()

    with allure.step("Проверяем наличие изображений в слайдере"):
        image_count = mobile_page.amenities.verify_slider_images()
        allure.attach(
            f"Количество изображений в слайдере: {image_count}", name="Image Count"
        )

    with allure.step("Проверяем наличие индикаторов слайдера"):
        indicator_count = mobile_page.amenities.verify_slider_indicators()
        allure.attach(
            f"Количество индикаторов: {indicator_count}", name="Indicator Count"
        )

    with allure.step("Тестируем навигацию по слайдеру - кликаем на стрелку вправо"):
        mobile_page.click_mobile_amenities_next_button()
        mobile_page.page.wait_for_timeout(1000)

    with allure.step(
        "Тестируем навигацию по слайдеру - еще раз кликаем на стрелку вправо"
    ):
        mobile_page.click_mobile_amenities_next_button()
        mobile_page.page.wait_for_timeout(1000)

    with allure.step("Закрываем модальное окно amenities"):
        mobile_page.amenities.close_modal()

    with allure.step("Проверяем, что модальное окно закрылось"):
        mobile_page.amenities.verify_modal_closed()

    with allure.step("Проверяем адаптивность на мобильном устройстве"):
        mobile_page.check_mobile_viewport_adaptation()
