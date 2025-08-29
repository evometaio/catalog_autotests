import allure
import pytest


@allure.feature("Страница проекта")
@allure.story("Загрузка PDF")
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.ui
@allure.severity(allure.severity_level.CRITICAL)
def test_download_pdf_on_agent_route(project_agent_page):
    downloaded_file_path = ""

    try:
        with allure.step("Открываем агентскую страницу"):
            project_agent_page.open_agent_page()

            current_url = project_agent_page.get_current_url()
            assert "agent" in current_url, "Не открылась агентская страница"

        with allure.step("Кликаем на проект Arisha"):
            project_agent_page.click_on_agent_project('arisha')

        with allure.step("Кликаем на кнопку All units"):
            project_agent_page.click_on_all_units_button('arisha')

        with allure.step("Кликаем на доступный апарт"):
            project_agent_page.click_on_avialable_apartment()

        with allure.step("Кликаем на кнопку Sales Offer и скачиваем PDF"):
            project_agent_page.click_on_sales_offer_button()

            # Скачиваем PDF и получаем путь к файлу
            success, file_path = project_agent_page.download_pdf_and_verify()
            assert success, "PDF не был скачан"

            downloaded_file_path = file_path

        with open(file_path, 'rb') as f:
            content = f.read(10)
            assert content.startswith(b'%PDF'), f"Файл не является валидным PDF: {content[:10]}"

    finally:
        # Очищаем скачанный файл в любом случае (успех или ошибка)
        if downloaded_file_path:
            with allure.step("Удаляем скачанный PDF файл"):
                project_agent_page.cleanup_after_test()