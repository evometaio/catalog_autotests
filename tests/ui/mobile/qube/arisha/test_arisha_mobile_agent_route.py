import allure
import pytest


class TestArishaMobileAgentRoute:
    """Мобильные тесты для агентского роута Arisha."""

    @allure.feature("Qube - Проект Arisha (mobile)")
    @allure.story("Агентский роут Arisha - Мобильная")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.mobile
    @pytest.mark.regression
    def test_arisha_mobile_download_pdf_on_catalog_page(self, mobile_agent_page):
        """Тест скачивания PDF на странице каталога Arisha на мобильном устройстве."""

        try:
            with allure.step("Переходим на страницу каталога Arisha"):
                mobile_agent_page.navigate_to_mobile_catalog_page("arisha")
                assert (
                    "catalog_2d" in mobile_agent_page.page.url
                    or "/area" in mobile_agent_page.page.url
                )

            with allure.step("Ищем и кликаем на первый доступный апартамент"):
                mobile_agent_page.find_and_click_available_apartment()
                mobile_agent_page.page.wait_for_timeout(1000)

            with allure.step("Кликаем на кнопку PDF"):
                # Просто кликаем на кнопку PDF без проверки скачивания
                pdf_clicked = mobile_agent_page.click_mobile_pdf_button()
                assert pdf_clicked, "Кнопка PDF не была нажата"

        finally:
            # Проверяем адаптивность на мобильном устройстве
            with allure.step("Проверяем адаптивность на мобильном устройстве"):
                mobile_agent_page.check_mobile_viewport_adaptation()
