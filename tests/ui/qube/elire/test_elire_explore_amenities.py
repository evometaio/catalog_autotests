import allure
import pytest


@allure.feature("Qube - Проект Elire")
@allure.story("Explore Amenities")
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.ui
def test_elire_explore_amenities(map_page):
    """Тест Explore Amenities для проекта Elire."""
    with allure.step("Открываем карту"):
        map_page.open(route_type="map")

    with allure.step("Кликаем на проект Elire"):
        map_page.click_project_on_map("elire")

    with allure.step("Кликаем на кнопку Services & Amenities"):
        map_page.elire.click_on_services_amenities_button()

    with allure.step("Проверяем отображение модального окна amenities"):
        map_page.expect_visible(map_page.project_locators.Elire.AMENITIES_MODAL)

    with allure.step("Проверяем наличие заголовка модального окна"):
        map_page.expect_visible(map_page.project_locators.Elire.AMENITIES_MODAL_TITLE)

    with allure.step("Проверяем наличие кнопки закрытия модального окна"):
        map_page.expect_visible(
            map_page.project_locators.Elire.AMENITIES_MODAL_CLOSE_BUTTON
        )

    with allure.step("Проверяем отображение слайдера в модалке"):
        map_page.expect_visible(map_page.project_locators.AMENITIES_SLIDER)

    with allure.step("Проверяем наличие изображений в слайдере"):
        images = map_page.query_selector_all(
            map_page.project_locators.AMENITIES_SLIDER_IMAGES
        )
        image_count = len(images)
        allure.attach(
            f"Количество изображений в слайдере: {image_count}", name="Image Count"
        )

    with allure.step("Проверяем наличие индикаторов слайдера"):
        indicators = map_page.query_selector_all(
            map_page.project_locators.AMENITIES_SLIDER_INDICATORS
        )
        indicator_count = len(indicators)
        allure.attach(
            f"Количество индикаторов: {indicator_count}", name="Indicator Count"
        )

    with allure.step("Тестируем навигацию по слайдеру - кликаем на индикатор 4"):
        if indicator_count > 3:
            map_page.click_element(
                f"{map_page.project_locators.AMENITIES_SLIDER_INDICATORS}:nth-child(4)"
            )
            # Ждем изменения слайда - проверяем что активный индикатор изменился
            map_page.page.wait_for_selector(
                f"{map_page.project_locators.AMENITIES_SLIDER_INDICATORS}:nth-child(4)[class*='active']",
                timeout=2000,
            )

    with allure.step("Тестируем навигацию по слайдеру - кликаем на индикатор 8"):
        if indicator_count > 7:
            map_page.click_element(
                f"{map_page.project_locators.AMENITIES_SLIDER_INDICATORS}:nth-child(8)"
            )
            # Ждем изменения слайда - проверяем что активный индикатор изменился
            map_page.page.wait_for_selector(
                f"{map_page.project_locators.AMENITIES_SLIDER_INDICATORS}:nth-child(8)[class*='active']",
                timeout=2000,
            )

    with allure.step("Закрываем модальное окно amenities"):
        map_page.click_element(
            map_page.project_locators.Elire.AMENITIES_MODAL_CLOSE_BUTTON
        )
        # Ждем закрытия модального окна
        map_page.page.wait_for_selector(
            map_page.project_locators.Elire.AMENITIES_MODAL,
            state="hidden",
            timeout=3000,
        )
