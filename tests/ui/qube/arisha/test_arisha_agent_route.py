import allure
import pytest


@allure.feature("Qube - Проект Arisha")
@allure.story("Агентский роут - Загрузка PDF")
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.ui
@pytest.mark.flaky(reruns=2, reruns_delay=4)
def test_arisha_download_pdf_on_agent_page(agent_page):
    """Тест скачивания PDF на агентской странице проекта Arisha."""
    downloaded_file_path = ""

    try:
        with allure.step("Открываем агентскую страницу"):
            agent_page.open(route_type="agent")

        with allure.step("Кликаем на проект Arisha"):
            agent_page.click_project_on_map("arisha")

        with allure.step("Кликаем на кнопку All units"):
            agent_page.project.click_on_all_units_button()
            agent_page.assert_url_contains(
                "catalog_2d", "Не перешли на страницу каталога"
            )

        with allure.step("Ищем и кликаем на первый доступный апартамент"):
            agent_page.project.find_and_click_available_apartment("arisha")
            agent_page.wait_for_timeout(1000)

        with allure.step("Кликаем на кнопку Sales Offer"):
            agent_page.project.click_on_sales_offer_button()

        with allure.step("Скачиваем PDF"):
            success, file_path = agent_page.project.download_pdf_and_verify()
            agent_page.assert_that(success, "PDF не был скачан")
            downloaded_file_path = file_path

        with allure.step("Проверяем что файл является валидным PDF"):
            with open(file_path, "rb") as f:
                content = f.read(10)
                agent_page.assert_that(
                    content.startswith(b"%PDF"),
                    f"Файл не является валидным PDF, заголовок: {content[:10]}",
                )

    finally:
        # Очищаем скачанный файл в любом случае
        if downloaded_file_path:
            with allure.step("Удаляем скачанный PDF файл"):
                agent_page.project.cleanup_pdf_after_test()
