import allure
import pytest


@allure.feature("Qube - Проект Cubix")
@allure.story("Агентский роут - Загрузка PDF")
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.ui
@pytest.mark.flaky(reruns=2, reruns_delay=4)
def test_cubix_download_pdf_on_agent_page(agent_page):
    """Тест скачивания PDF на агентской странице проекта Cubix."""
    downloaded_file_path = ""

    try:
        with allure.step("Открываем агентскую страницу"):
            agent_page.open(route_type="agent")

        with allure.step("Кликаем на проект Cubix"):
            agent_page.click_project_on_map("cubix")

        with allure.step("Ищем и кликаем на первый доступный апартамент"):
            agent_page.project.find_and_click_available_apartment("cubix")

        with allure.step("Кликаем на кнопку Sales Offer"):
            agent_page.project.click_on_sales_offer_button()

        with allure.step("Скачиваем PDF"):
            success, file_path = agent_page.project.download_pdf_and_verify()
            assert success, "PDF не был скачан"
            downloaded_file_path = file_path

        with allure.step("Проверяем что файл является валидным PDF"):
            with open(file_path, "rb") as f:
                content = f.read(10)
                assert content.startswith(
                    b"%PDF"
                ), f"Файл не является валидным PDF: {content[:10]}"

    finally:
        # Очищаем скачанный файл в любом случае (успех или ошибка)
        if downloaded_file_path:
            with allure.step("Удаляем скачанный PDF файл"):
                agent_page.project.cleanup_pdf_after_test()
