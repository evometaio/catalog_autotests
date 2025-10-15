import allure
import pytest


class TestArishaMobileAgentRoute:
    """Мобильные тесты для агентского роута Arisha."""

    @allure.feature("Qube - Проект Arisha (mobile)")
    @allure.story("Агентский роут Arisha - Мобильная")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.mobile
    @pytest.mark.regression
    @pytest.mark.flaky(reruns=2, reruns_delay=4)
    def test_arisha_mobile_download_pdf_on_catalog_page(self, mobile_page):
        """Тест скачивания PDF на странице каталога Arisha на мобильном устройстве."""

        try:
            with allure.step("Переходим на страницу каталога Arisha"):
                mobile_page.navigate_to_mobile_catalog_page("arisha")
                current_url = mobile_page.page.url
                mobile_page.assertions.assert_that(
                    "catalog_2d" in current_url or "/area" in current_url,
                    "Не перешли на страницу каталога или area",
                )

            with allure.step("Ищем и кликаем на первый доступный апартамент"):
                mobile_page.mobile_navigation.find_and_click_available_apartment()
                mobile_page.page.wait_for_timeout(1000)

            with allure.step("Кликаем на кнопку PDF"):
                pdf_clicked = mobile_page.click_mobile_pdf_button()
                mobile_page.assertions.assert_that(
                    pdf_clicked, "Кнопка PDF не была нажата"
                )

        finally:
            # Проверяем адаптивность на мобильном устройстве
            with allure.step("Проверяем адаптивность на мобильном устройстве"):
                mobile_page.check_mobile_viewport_adaptation()
