import os

import allure
import pytest

from pages.page_factory import PageFactory


@allure.feature("Qube - Проект Elire")
@allure.story("Explore Amenities")
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.ui
@pytest.mark.skipif(
    os.getenv("TEST_ENVIRONMENT", "dev") == "prod",
    reason="тест временно отключен на PROD",
)
def test_elire_explore_amenities(map_page):
    """Тест Explore Amenities для проекта Elire."""
    with allure.step("Открываем карту"):
        map_page.open(route_type="map")

    with allure.step("Кликаем на проект Elire"):
        map_page.click_project_on_map("elire")

    with allure.step("Кликаем на кнопку Residences"):
        qube_pages = PageFactory.get_page_object(map_page.page, "qube")
        qube_pages.click_on_residences_button()

    with allure.step("Проверяем наличие кнопки SERVICES & AMENITIES"):
        qube_pages.expect_visible(
            qube_pages.project_locators.Elire.EXPLORE_AMENITIES_BUTTON
        )

    with allure.step("Кликаем на кнопку Explore Amenities"):
        qube_pages.click_element(
            qube_pages.project_locators.Elire.EXPLORE_AMENITIES_BUTTON
        )

    with allure.step("Проверяем отображение модального окна amenities"):
        qube_pages.expect_visible(qube_pages.project_locators.Elire.AMENITIES_MODAL)

    with allure.step("Проверяем наличие заголовка модального окна"):
        qube_pages.expect_visible(
            qube_pages.project_locators.Elire.AMENITIES_MODAL_TITLE
        )

    with allure.step("Проверяем наличие кнопки закрытия модального окна"):
        qube_pages.expect_visible(
            qube_pages.project_locators.Elire.AMENITIES_MODAL_CLOSE_BUTTON
        )

    with allure.step("Проверяем отображение слайдера в модалке"):
        qube_pages.expect_visible(qube_pages.project_locators.AMENITIES_SLIDER)

    with allure.step("Проверяем наличие изображений в слайдере"):
        images = qube_pages.query_selector_all(
            qube_pages.project_locators.AMENITIES_SLIDER_IMAGES
        )
        image_count = len(images)
        allure.attach(
            f"Количество изображений в слайдере: {image_count}", name="Image Count"
        )

    with allure.step("Проверяем наличие индикаторов слайдера"):
        indicators = qube_pages.query_selector_all(
            qube_pages.project_locators.AMENITIES_SLIDER_INDICATORS
        )
        indicator_count = len(indicators)
        allure.attach(
            f"Количество индикаторов: {indicator_count}", name="Indicator Count"
        )

    with allure.step("Тестируем навигацию по слайдеру - кликаем на индикатор 4"):
        if indicator_count > 3:
            qube_pages.click_element(
                f"{qube_pages.project_locators.AMENITIES_SLIDER_INDICATORS}:nth-child(4)"
            )
            # Ждем изменения слайда - проверяем что активный индикатор изменился
            qube_pages.page.wait_for_selector(
                f"{qube_pages.project_locators.AMENITIES_SLIDER_INDICATORS}:nth-child(4)[class*='active']",
                timeout=2000,
            )

    with allure.step("Тестируем навигацию по слайдеру - кликаем на индикатор 8"):
        if indicator_count > 7:
            qube_pages.click_element(
                f"{qube_pages.project_locators.AMENITIES_SLIDER_INDICATORS}:nth-child(8)"
            )
            # Ждем изменения слайда - проверяем что активный индикатор изменился
            qube_pages.page.wait_for_selector(
                f"{qube_pages.project_locators.AMENITIES_SLIDER_INDICATORS}:nth-child(8)[class*='active']",
                timeout=2000,
            )

    with allure.step("Закрываем модальное окно amenities"):
        qube_pages.click_element(
            qube_pages.project_locators.Elire.AMENITIES_MODAL_CLOSE_BUTTON
        )
        # Ждем закрытия модального окна
        qube_pages.page.wait_for_selector(
            qube_pages.project_locators.Elire.AMENITIES_MODAL,
            state="hidden",
            timeout=3000,
        )

    with allure.step("Проверяем, что модальное окно закрылось"):
        assert not qube_pages.is_element_visible(
            qube_pages.project_locators.Elire.AMENITIES_MODAL
        ), "Модальное окно amenities все еще видно"
