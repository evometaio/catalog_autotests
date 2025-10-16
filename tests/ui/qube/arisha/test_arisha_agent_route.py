import allure
import pytest


@allure.feature("Qube - Проект Arisha")
@allure.story("Агентский роут - Загрузка PDF")
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.ui
@pytest.mark.flaky(reruns=2, reruns_delay=2)
def test_arisha_download_pdf_on_agent_page(arisha_page):
    """Тест скачивания PDF на агентской странице проекта Arisha."""
    downloaded_file_path = ""

    try:
        with allure.step("Открываем агентскую страницу"):
            arisha_page.open(route_type="agent")

        with allure.step("Кликаем на проект Arisha"):
            arisha_page.map.navigate_to_project("arisha")

        with allure.step("Кликаем на кнопку All units"):
            arisha_page.click_all_units_button()
            arisha_page.assertions.assert_url_contains(
                "catalog_2d", "Не перешли на страницу каталога"
            )

        with allure.step("Ищем и кликаем на первый доступный апартамент"):
            arisha_page.navigation.find_and_click_available_apartment()
            arisha_page.browser.wait_for_timeout(1000)

        with allure.step("Кликаем на кнопку Sales Offer"):
            arisha_page.click_sales_offer_button()

        with allure.step("Скачиваем PDF"):
            success, file_path = arisha_page.download_pdf_and_verify()
            arisha_page.assertions.assert_that(success, "PDF не был скачан")
            downloaded_file_path = file_path

        with allure.step("Проверяем что файл является валидным PDF"):
            with open(file_path, "rb") as f:
                content = f.read(10)
                arisha_page.assertions.assert_that(
                    content.startswith(b"%PDF"),
                    f"Файл не является валидным PDF, заголовок: {content[:10]}",
                )

    finally:
        # Очищаем скачанный файл в любом случае
        if downloaded_file_path:
            with allure.step("Удаляем скачанный PDF файл"):
                arisha_page.cleanup_pdf_after_test()
