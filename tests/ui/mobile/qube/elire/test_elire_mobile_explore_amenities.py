import allure
import pytest


@allure.feature("Qube - Проект Elire (mobile")
@allure.story("Explore Amenities")
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.ui
@pytest.mark.parametrize("route_type", ["map", "agent", "client"])
@pytest.mark.skip(reason="Пофиксить")
def test_elire_mobile_explore_amenities(mobile_page, route_type):
    """Тест Explore Amenities для проекта Elire на всех роутах."""
    with allure.step(f"Открываем страницу {route_type}"):
        mobile_page.open(route_type=route_type)

    with allure.step("Кликаем на проект Elire"):
        mobile_page.map.navigate_to_project("elire")

    with allure.step("Кликаем на кнопку Services & Amenities"):
        mobile_page.click_services_amenities_button()

    with allure.step("Проверяем отображение модального окна amenities"):
        mobile_page.browser.expect_visible(mobile_page.project_locators.AMENITIES_MODAL)

    with allure.step("Проверяем наличие заголовка модального окна"):
        # У Elire используем специфичный data-test-id вместо общего селектора h3
        mobile_page.browser.expect_visible(
            '[data-test-id="public-zone-info-slider-title"]'
        )

    with allure.step("Проверяем наличие кнопки закрытия модального окна"):
        mobile_page.browser.expect_visible(
            mobile_page.project_locators.AMENITIES_MODAL_CLOSE_BUTTON
        )

    with allure.step("Проверяем отображение слайдера в модалке"):
        mobile_page.browser.expect_visible(mobile_page.project_locators.AMENITIES_SLIDER)

    with allure.step("Проверяем наличие изображений в слайдере"):
        images = mobile_page.browser.query_selector_all(
            mobile_page.project_locators.AMENITIES_SLIDER_IMAGES
        )
        image_count = len(images)
        allure.attach(
            f"Количество изображений в слайдере: {image_count}", name="Image Count"
        )

    with allure.step("Проверяем наличие индикаторов слайдера"):
        indicators = mobile_page.browser.query_selector_all(
            mobile_page.project_locators.AMENITIES_SLIDER_INDICATORS
        )
        indicator_count = len(indicators)
        allure.attach(
            f"Количество индикаторов: {indicator_count}", name="Indicator Count"
        )

    with allure.step("Тестируем навигацию по слайдеру - кликаем на индикатор 4"):
        if indicator_count > 3:
            mobile_page.browser.click(
                f"{mobile_page.project_locators.AMENITIES_SLIDER_INDICATORS}:nth-child(4)"
            )
            # Ждем изменения слайда
            mobile_page.page.wait_for_selector(
                f"{mobile_page.project_locators.AMENITIES_SLIDER_INDICATORS}:nth-child(4)[class*='active']",
                timeout=2000,
            )

    with allure.step("Тестируем навигацию по слайдеру - кликаем на индикатор 8"):
        if indicator_count > 7:
            mobile_page.browser.click(
                f"{mobile_page.project_locators.AMENITIES_SLIDER_INDICATORS}:nth-child(8)"
            )
            # Ждем изменения слайда
            mobile_page.page.wait_for_selector(
                f"{mobile_page.project_locators.AMENITIES_SLIDER_INDICATORS}:nth-child(8)[class*='active']",
                timeout=2000,
            )

    with allure.step("Закрываем модальное окно amenities"):
        mobile_page.browser.click(
            mobile_page.project_locators.AMENITIES_MODAL_CLOSE_BUTTON
        )
        # Ждем закрытия модального окна
        mobile_page.page.wait_for_selector(
            mobile_page.project_locators.AMENITIES_MODAL,
            state="hidden",
            timeout=3000,
        )
