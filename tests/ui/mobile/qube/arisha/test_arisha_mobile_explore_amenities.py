import allure
import pytest


@allure.feature("Qube - Проект Arisha (mobile)")
@allure.story("Explore Amenities - Мобильная")
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.mobile
def test_arisha_mobile_explore_amenities(mobile_page):
    """Тест Explore Amenities для проекта Arisha на мобильном устройстве."""
    with allure.step("Открываем карту"):
        mobile_page.open(route_type="map")

    with allure.step("Кликаем на проект Arisha на карте"):
        mobile_page.click_mobile_project_on_map("arisha")

    with allure.step("Кликаем на Explore Project"):
        mobile_page.click_mobile_explore_project_button("arisha")

    with allure.step("Открываем мобильное меню Arisha"):
        mobile_menu_toggle = mobile_page.page.locator(
            '[data-test-id="nav-mobile-menu-toggle"]'
        )
        mobile_menu_toggle.wait_for(state="visible", timeout=10000)
        mobile_menu_toggle.click()
        mobile_page.page.wait_for_timeout(1000)

    with allure.step("Кликаем на All Units в меню"):
        all_units_button = mobile_page.page.locator(
            '[data-test-id="nav-mobile-catalog2d"]'
        )
        all_units_button.wait_for(state="visible", timeout=10000)
        all_units_button.click()
        mobile_page.page.wait_for_timeout(1000)

    with allure.step("Кликаем на кнопку Explore Amenities"):
        mobile_page.click_mobile_explore_amenities_button()

    with allure.step("Проверяем отображение модального окна amenities"):
        mobile_page.verify_amenities_modal_displayed()

    with allure.step("Проверяем наличие заголовка модального окна"):
        mobile_page.verify_amenities_modal_title()

    with allure.step("Проверяем наличие кнопки закрытия модального окна"):
        mobile_page.verify_amenities_modal_close_button()

    with allure.step("Проверяем отображение слайдера в модалке"):
        mobile_page.verify_amenities_slider_displayed()

    with allure.step("Проверяем наличие изображений в слайдере"):
        image_count = mobile_page.verify_amenities_slider_images()
        allure.attach(
            f"Количество изображений в слайдере: {image_count}", name="Image Count"
        )

    with allure.step("Проверяем наличие индикаторов слайдера"):
        indicator_count = mobile_page.verify_amenities_slider_indicators()
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
        mobile_page.close_amenities_modal()

    with allure.step("Проверяем, что модальное окно закрылось"):
        mobile_page.verify_amenities_modal_closed()

    with allure.step("Проверяем адаптивность на мобильном устройстве"):
        mobile_page.check_mobile_viewport_adaptation()
