import allure
import pytest


class TestCubixMobileAgentRoute:
    """Мобильные тесты для агентского роута Cubix."""

    @allure.feature("Qube - Проект Cubix (mobile)")
    @allure.story("Агентский роут Cubix - Мобильная")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.mobile
    @pytest.mark.regression
    def test_cubix_mobile_download_pdf_on_catalog_page(self, mobile_agent_page):
        """Тест скачивания PDF на странице каталога Cubix на мобильном устройстве."""

        try:
            with allure.step("Переходим на карту агента"):
                mobile_agent_page.page.goto(mobile_agent_page.agent_base_url)
                mobile_agent_page.page.wait_for_load_state("domcontentloaded")

            with allure.step("Кликаем на проект Cubix на карте"):
                mobile_agent_page.click_mobile_project_on_map("cubix")

            with allure.step("Кликаем на Explore Project"):
                mobile_agent_page.click_mobile_explore_project_button("cubix")

            with allure.step("Ищем и кликаем на первый доступный апартамент"):
                mobile_agent_page.find_and_click_available_apartment()
                mobile_agent_page.page.wait_for_timeout(1000)

            with allure.step("Кликаем на кнопку PDF"):
                pdf_clicked = mobile_agent_page.click_mobile_pdf_button()
                mobile_agent_page.assert_that(pdf_clicked, "Кнопка PDF не была нажата")

        finally:
            # Проверяем адаптивность на мобильном устройстве
            with allure.step("Проверяем адаптивность на мобильном устройстве"):
                mobile_agent_page.check_mobile_viewport_adaptation()

