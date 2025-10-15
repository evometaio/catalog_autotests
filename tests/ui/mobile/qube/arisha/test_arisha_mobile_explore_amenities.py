import allure
import pytest


@allure.feature("Qube - Проект Arisha (mobile)")
@allure.story("Explore Amenities - Мобильная")
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.mobile
@pytest.mark.flaky(reruns=2, reruns_delay=4)
@pytest.mark.parametrize("route_type", ["map", "agent", "client"])
def test_arisha_mobile_explore_amenities(mobile_page, route_type):
    """Тест Explore Amenities для проекта Arisha на мобильном устройстве на всех роутах."""
    with allure.step(f"Открываем страницу {route_type}"):
        mobile_page.open(route_type=route_type)

    with allure.step("Кликаем на проект Arisha на карте"):
        mobile_page.mobile_map.click_project("arisha")

    with allure.step("Кликаем на Explore Project"):
        mobile_page.mobile_map.click_explore_project("arisha")

    mobile_page.navigate_to_mobile_arisha_all_units()

    with allure.step("Кликаем на кнопку Explore Amenities"):
        mobile_page.click_mobile_explore_amenities_button()

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
