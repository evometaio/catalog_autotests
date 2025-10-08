import allure
import pytest


@allure.feature("Qube - Проект Cubix (mobile)")
@allure.story("Explore Amenities - Мобильная")
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.mobile
def test_cubix_mobile_explore_amenities(mobile_page):
    """Тест Explore Amenities для проекта Cubix на мобильном устройстве."""
    
    with allure.step("Открываем карту на мобильном устройстве"):
        mobile_page.page.goto(mobile_page.base_url)

    with allure.step("Кликаем на проект Cubix на карте"):
        mobile_page.click_mobile_project_on_map("cubix")

    with allure.step("Кликаем на Explore Project"):
        mobile_page.click_mobile_explore_project_button("cubix")

    with allure.step("Проверяем наличие кнопки Explore Amenities"):
        from locators.mobile_locators import MOBILE_EXPLORE_AMENITIES_BUTTON
        mobile_page.expect_visible(MOBILE_EXPLORE_AMENITIES_BUTTON)

    with allure.step("Кликаем на кнопку Explore Amenities"):
        from locators.mobile_locators import MOBILE_EXPLORE_AMENITIES_BUTTON
        mobile_page.click(MOBILE_EXPLORE_AMENITIES_BUTTON)

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
        # На мобильной версии используем стрелки вместо индикаторов
        from locators.mobile_locators import MOBILE_AMENITIES_SLIDER_NEXT_BUTTON
        next_button = mobile_page.page.locator(MOBILE_AMENITIES_SLIDER_NEXT_BUTTON)
        next_button.click()
        mobile_page.page.wait_for_timeout(1000)

    with allure.step("Тестируем навигацию по слайдеру - еще раз кликаем на стрелку вправо"):
        from locators.mobile_locators import MOBILE_AMENITIES_SLIDER_NEXT_BUTTON
        next_button = mobile_page.page.locator(MOBILE_AMENITIES_SLIDER_NEXT_BUTTON)
        next_button.click()
        mobile_page.page.wait_for_timeout(1000)

    with allure.step("Закрываем модальное окно amenities"):
        mobile_page.close_amenities_modal()

    with allure.step("Проверяем, что модальное окно закрылось"):
        mobile_page.verify_amenities_modal_closed()

    # Проверяем адаптивность на мобильном устройстве
    with allure.step("Проверяем адаптивность на мобильном устройстве"):
        mobile_page.check_mobile_viewport_adaptation()

