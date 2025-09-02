import allure
import pytest


@allure.feature("Qube - Проект Elire")
@allure.story("Агентский роут - Загрузка PDF")
@pytest.mark.smoke
@pytest.mark.skip(reason="Нет такого функционала")
@pytest.mark.regression
@pytest.mark.ui
def test_elire_download_pdf_on_agent_page(elire_agent_page):
    """Тест скачивания PDF на агентской странице проекта Elire."""
    downloaded_file_path = ""

    try:
        with allure.step("Открываем агентскую страницу проекта Elire"):
            elire_agent_page.open_agent_page()

            current_url = elire_agent_page.get_current_url()
            assert "agent" in current_url, "Не открылась агентская страница"

        with allure.step("Кликаем на проект Elire"):
            elire_agent_page.click_on_project("elire")

        with allure.step("Кликаем на главное здание"):
            elire_agent_page.click_on_all_units_button()

        with allure.step("Ищем и кликаем на первый доступный апартамент"):
            selected_apartment = elire_agent_page.find_and_click_available_apartment()
            print(f"Выбран апартамент: {selected_apartment}")

        with allure.step("Кликаем на кнопку Sales Offer и скачиваем PDF"):
            elire_agent_page.click_on_sales_offer_button()

            # Скачиваем PDF и получаем путь к файлу
            success, file_path = elire_agent_page.download_pdf_and_verify()
            assert success, "PDF не был скачан"

            downloaded_file_path = file_path

        with open(file_path, "rb") as f:
            content = f.read(10)
            assert content.startswith(
                b"%PDF"
            ), f"Файл не является валидным PDF: {content[:10]}"

    finally:
        # Очищаем скачанный файл в любом случае (успех или ошибка)
        if downloaded_file_path:
            with allure.step("Удаляем скачанный PDF файл"):
                elire_agent_page.cleanup_pdf_after_test()
