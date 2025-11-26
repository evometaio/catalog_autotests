import allure
import pytest


@allure.feature("Vibe - Проект Arsenal (mobile)")
@allure.story("Навигация в каталог")
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.mobile
def test_arsenal_mobile_catalog_navigation(mobile_page):
    """Тест перехода в каталог квартир Arsenal на мобильном устройстве."""
    with allure.step("Открываем страницу map"):
        mobile_page.open(route_type="map")

    with allure.step("Переходим в каталог через навигацию"):
        mobile_page.navigate_to_mobile_catalog_page("arsenal")

    with allure.step("Проверяем наличие кнопок квартир в каталоге"):
        property_buttons = mobile_page.page.locator(
            '[data-test-id^="property-info-primary-button-"]'
        )
        property_buttons.first.wait_for(state="attached", timeout=10000)
        assert property_buttons.count() > 0, "Не найдено кнопок квартир в каталоге"

    with allure.step("Проверяем адаптивность на мобильном устройстве"):
        mobile_page.check_mobile_viewport_adaptation()
