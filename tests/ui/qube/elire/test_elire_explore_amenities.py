import allure
import pytest


@allure.feature("Qube - Проект Elire")
@allure.story("Explore Amenities")
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.ui
def test_elire_explore_amenities(elire_page):
    """Тест Explore Amenities для проекта Elire."""
    with allure.step("Открываем карту"):
        elire_page.open(route_type="map")

    with allure.step("Кликаем на проект Elire"):
        elire_page.map.navigate_to_project("elire")

    with allure.step("Кликаем на кнопку Services & Amenities"):
        elire_page.click_services_amenities_button()

    with allure.step("Проверяем отображение модального окна amenities"):
        elire_page.browser.expect_visible(elire_page.project_locators.AMENITIES_MODAL)

    with allure.step("Проверяем наличие заголовка модального окна"):
        elire_page.browser.expect_visible(elire_page.project_locators.AMENITIES_MODAL_TITLE)

    with allure.step("Проверяем наличие кнопки закрытия модального окна"):
        elire_page.browser.expect_visible(
            elire_page.project_locators.AMENITIES_MODAL_CLOSE_BUTTON
        )

    with allure.step("Проверяем отображение слайдера в модалке"):
        elire_page.browser.expect_visible(elire_page.project_locators.AMENITIES_SLIDER)

    with allure.step("Проверяем наличие изображений в слайдере"):
        images = elire_page.browser.query_selector_all(
            elire_page.project_locators.AMENITIES_SLIDER_IMAGES
        )
        image_count = len(images)
        allure.attach(
            f"Количество изображений в слайдере: {image_count}", name="Image Count"
        )

    with allure.step("Проверяем наличие индикаторов слайдера"):
        indicators = elire_page.browser.query_selector_all(
            elire_page.project_locators.AMENITIES_SLIDER_INDICATORS
        )
        indicator_count = len(indicators)
        allure.attach(
            f"Количество индикаторов: {indicator_count}", name="Indicator Count"
        )

    with allure.step("Тестируем навигацию по слайдеру - кликаем на индикатор 4"):
        if indicator_count > 3:
            elire_page.browser.click(
                f"{elire_page.project_locators.AMENITIES_SLIDER_INDICATORS}:nth-child(4)"
            )
            # Ждем изменения слайда
            elire_page.page.wait_for_selector(
                f"{elire_page.project_locators.AMENITIES_SLIDER_INDICATORS}:nth-child(4)[class*='active']",
                timeout=2000,
            )

    with allure.step("Тестируем навигацию по слайдеру - кликаем на индикатор 8"):
        if indicator_count > 7:
            elire_page.browser.click(
                f"{elire_page.project_locators.AMENITIES_SLIDER_INDICATORS}:nth-child(8)"
            )
            # Ждем изменения слайда
            elire_page.page.wait_for_selector(
                f"{elire_page.project_locators.AMENITIES_SLIDER_INDICATORS}:nth-child(8)[class*='active']",
                timeout=2000,
            )

    with allure.step("Закрываем модальное окно amenities"):
        elire_page.browser.click(
            elire_page.project_locators.AMENITIES_MODAL_CLOSE_BUTTON
        )
        # Ждем закрытия модального окна
        elire_page.page.wait_for_selector(
            elire_page.project_locators.AMENITIES_MODAL,
            state="hidden",
            timeout=3000,
        )
