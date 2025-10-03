"""
Мобильные тесты для Arisha Agent Route.
Тесты адаптированы для работы на мобильных устройствах с соответствующими локаторами.
"""

import pytest
import allure
from playwright.sync_api import Page
from pages.mobile_page import MobilePage


class TestArishaMobileAgentRoute:
    """Мобильные тесты для агентского роута Arisha."""

    @allure.story("Arisha Agent Route - Mobile")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.mobile
    @pytest.mark.regression
    def test_arisha_mobile_download_pdf_on_catalog_page(self, page: Page):
        """Тест скачивания PDF на странице каталога Arisha на мобильном устройстве."""
        mobile_page = MobilePage(page)
        
        with allure.step("Скачиваем PDF файл каталога Arisha на мобильном устройстве"):
            # Используем мобильный метод для скачивания PDF с каталога
            filename = mobile_page.download_mobile_pdf("arisha", "catalog")
            
            # Проверяем успешность скачивания
            assert filename is not None, "PDF файл не был скачан"
            print(f"✅ PDF файл успешно скачан: {filename}")
        
        with allure.step("Проверяем адаптивность на мобильном устройстве"):
            mobile_page.check_mobile_viewport_adaptation()

    @allure.story("Arisha Agent Route - Mobile")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.mobile
    @pytest.mark.smoke
    def test_arisha_mobile_agent_page_loads(self, page: Page):
        """Тест загрузки страницы агента Arisha на мобильном устройстве."""
        mobile_page = MobilePage(page)
        
        with allure.step("Переходим напрямую на страницу агента Arisha"):
            page.goto("https://qube-dev-next.evometa.io/arisha/agent/")
            page.wait_for_load_state("domcontentloaded")
        
        with allure.step("Проверяем загрузку страницы"):
            # Проверяем основные элементы страницы
            title_selectors = [
                'h1',
                'h2', 
                '[data-testid*="title"]',
                '.page-title'
            ]
            
            title_found = False
            for selector in title_selectors:
                elements = page.locator(selector)
                if elements.count() > 0:
                    title_found = True
                    break
            
            assert title_found, "Заголовок страницы не найден"
            
        with allure.step("Проверяем адаптивность на мобильном устройстве"):
            mobile_page.check_mobile_viewport_adaptation()
            mobile_page.check_mobile_touch_elements()
