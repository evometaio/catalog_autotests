"""
Мобильные тесты для навигации по проектам QUBE на карте.
Тесты адаптированы для работы на мобильных устройствах с соответствующими локаторами.
"""

import pytest
import allure
from playwright.sync_api import Page
from pages.mobile_page import MobilePage


class TestQubeMobileMapProjects:
    """Мобильные тесты для навигации по проектам на карте."""

    @allure.story("Mobile Map Navigation - QUBE Projects")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.mobile
    @pytest.mark.regression
    @pytest.mark.parametrize("project_name", ["elire", "arisha", "cubix"])
    def test_mobile_project_navigation_on_map(self, page: Page, project_name: str):
        """Тест навигации по проектам на мобильном устройстве."""
        mobile_page = MobilePage(page)
        
        with allure.step(f"Открываем страницу карты"):
            mobile_page.open(route_type="map")
        
        with allure.step(f"Кликаем по проекту {project_name.upper()}"):
            mobile_page.click_mobile_project_on_map(project_name)
        
        with allure.step(f"Проверяем информацию о проекте {project_name.upper()}"):
            # Проверяем, что модальное окно с информацией о проекте видимо
            mobile_modal = page.locator(mobile_page.MOBILE_PROJECT_INFO_MODAL)
            assert mobile_modal.is_visible(), f"Модальное окно с информацией о проекте {project_name} не видимо"
            
            # Проверяем наличие кнопки Explore Project
            explore_button = page.locator(mobile_page.MOBILE_EXPLORE_BUTTON)
            assert explore_button.is_visible(), f"Кнопка Explore Project не видна для проекта {project_name}"
        
        with allure.step("Проверяем мобильную адаптивность"):
            mobile_page.check_mobile_viewport_adaptation()
            mobile_page.check_mobile_modal_behavior()

    @allure.story("Mobile Map Navigation - QUBE Projects")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.mobile
    @pytest.mark.parametrize("project_name", ["elire", "arisha", "cubix"])
    def test_mobile_project_full_navigation(self, page: Page, project_name: str):
        """Тест полной навигации от карты до страницы проекта на мобильном устройстве."""
        
        with allure.step(f"Открываем страницу карты"):
            page.goto("https://qube-dev-next.evometa.io/map")
            page.wait_for_load_state("domcontentloaded")
        
        with allure.step(f"Кликаем по проекту {project_name.upper()}"):
            # Используем мобильные локаторы для проектов
            project_selectors = {
                "arisha": 'div[aria-label="ARISHA TERACCES"]',
                "elire": 'div[aria-label="ELIRE"]',
                "cubix": 'div[aria-label="CUBIX RESIDENCE"]'
            }
            
            selector = project_selectors.get(project_name)
            assert selector, f"Не найден селектор для проекта {project_name}"
            
            project_element = page.locator(selector)
            assert project_element.count() > 0, f"Проект {project_name} не найден на карте"
            project_element.click()
            
            # Ждем появления мобильного модального окна
            mobile_modal = page.locator('div.ant-modal[class*="_popup"]')
            mobile_modal.wait_for(state="visible", timeout=10000)
        
        with allure.step(f"Кликаем на кнопку Explore Project для {project_name.upper()}"):
            explore_button = page.locator('//span[text()="Explore Project"]')
            assert explore_button.is_visible(), f"Кнопка Explore Project не видна для проекта {project_name}"
            explore_button.click()
            
            # Ждем перехода на страницу проекта
            expected_url_pattern = f"**/{project_name}/**"
            page.wait_for_url(expected_url_pattern, timeout=10000)
        
        with allure.step(f"Проверяем загрузку страницы проекта {project_name.upper()}"):
            # Проверяем, что мы на правильной странице
            current_url = page.url
            assert f"/{project_name}/" in current_url, f"URL не содержит название проекта {project_name}: {current_url}"
            
            # Проверяем наличие основных элементов страницы
            title_elements = page.locator('h1, h2, h3').all()
            assert len(title_elements) > 0, f"Не найдены заголовки на странице проекта {project_name}"
            
            # Проверяем адаптивность на мобильном устройстве
            viewport_width = page.viewport_size['width']
            assert viewport_width <= 768, f"Viewport слишком широкий для мобильного: {viewport_width}px"

    @allure.story("Mobile Map - Basic Functionality")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.mobile
    @pytest.mark.smoke
    def test_mobile_map_page_loads(self, page: Page):
        """Тест загрузки страницы карты на мобильном устройстве."""
        
        with allure.step("Открываем страницу карты"):
            page.goto("https://qube-dev-next.evometa.io/map")
            page.wait_for_load_state("domcontentloaded")
        
        with allure.step("Проверяем загрузку карты"):
            # Проверяем наличие контейнера карты
            map_container = page.locator('[data-testid="map"]')
            assert map_container.is_visible(), "Контейнер карты не виден"
            
            # Проверяем наличие проектов на карте
            projects = page.locator('div[aria-label*="ARISHA"], div[aria-label*="ELIRE"], div[aria-label*="CUBIX"]')
            assert projects.count() > 0, "Проекты не найдены на карте"
        
        with allure.step("Проверяем адаптивность карты на мобильном устройстве"):
            # Проверяем размер viewport
            viewport_width = page.viewport_size['width']
            viewport_height = page.viewport_size['height']
            
            assert viewport_width <= 768, f"Viewport слишком широкий для мобильного: {viewport_width}px"
            assert viewport_height <= 1024, f"Viewport слишком высокий для мобильного: {viewport_height}px"
            
            # Проверяем отсутствие горизонтальной прокрутки
            body_width = page.evaluate("document.body.scrollWidth")
            assert body_width <= viewport_width, "Карта требует горизонтальной прокрутки на мобильном"
