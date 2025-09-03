import time

import allure
import pytest


@allure.feature("Qube - Проект Arisha")
@allure.story("Агентский роут - Загрузка PDF")
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.ui
def test_arisha_download_pdf_on_agent_page(agent_page):
    """Тест скачивания PDF на агентской странице проекта Arisha."""
    downloaded_file_path = ""
    
    try:
        with allure.step("Открываем агентскую страницу"):
            agent_page.open(route_type="agent")
        
        with allure.step("Кликаем на проект Arisha"):
            agent_page.click_on_project("arisha")
            assert 'area' in agent_page.get_current_url()
        
        with allure.step("Кликаем на кнопку All units"):
            agent_page.click_on_all_units_button()
            assert 'catalog_2d' in agent_page.get_current_url()
        
        with allure.step("Ищем и кликаем на первый доступный апартамент"):
            agent_page.find_and_click_available_apartment("arisha")
        
        with allure.step("Кликаем на кнопку Sales Offer"):
            agent_page.click_on_sales_offer_button()
        
        with allure.step("Скачиваем PDF"):
            success, file_path = agent_page.download_pdf_and_verify()
            assert success, "PDF не был скачан"
            downloaded_file_path = file_path
        
        with allure.step("Проверяем что файл является валидным PDF"):
            with open(file_path, "rb") as f:
                content = f.read(10)
                assert content.startswith(b"%PDF"), f"Файл не является валидным PDF: {content[:10]}"
    
    finally:
        # Очищаем скачанный файл в любом случае (успех или ошибка)
        if downloaded_file_path:
            with allure.step("Удаляем скачанный PDF файл"):
                agent_page.cleanup_pdf_after_test()
