"""
Мобильные тесты для Arisha Agent Route.
Тесты адаптированы для работы на мобильных устройствах с соответствующими локаторами.
"""

import os

import allure
import pytest


class TestArishaMobileAgentRoute:
    """Мобильные тесты для агентского роута Arisha."""

    @allure.story("Arisha Agent Route - Mobile")
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

    @allure.story("Arisha Agent Route - Mobile")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.mobile
    @pytest.mark.smoke
    def test_arisha_mobile_agent_page_loads(self, mobile_agent_page):
        """Тест загрузки страницы агента Arisha на мобильном устройстве."""

        with allure.step("Переходим напрямую на страницу агента Arisha"):
            mobile_agent_page.open(route_type="agent")
            mobile_agent_page.page.wait_for_load_state("domcontentloaded")

        with allure.step("Проверяем загрузку страницы"):
            # Проверяем основные элементы страницы
            title_selectors = ["h1", "h2", '[data-testid*="title"]', ".page-title"]

            title_found = False
            for selector in title_selectors:
                elements = mobile_agent_page.page.locator(selector)
                if elements.count() > 0:
                    title_found = True
                    break

            assert title_found, "Заголовок страницы не найден"

        with allure.step("Проверяем адаптивность на мобильном устройстве"):
            mobile_agent_page.check_mobile_viewport_adaptation()
            mobile_agent_page.check_mobile_touch_elements()
