import allure
import pytest


@allure.feature("Qube - Проект Cubix")
@allure.story("Скачивание PDF предложения")
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.ui
@pytest.mark.flaky(reruns=2, reruns_delay=2)
def test_cubix_download_pdf_on_agent_page(cubix_page):
    """Тест скачивания PDF на агентской странице проекта Cubix."""
    downloaded_file_path = ""

    try:
        with allure.step("Открываем агентскую страницу"):
            cubix_page.open(route_type="agent")

        with allure.step("Кликаем на проект Cubix"):
            cubix_page.map.navigate_to_project("cubix")

        with allure.step("Ищем и кликаем на первый доступный апартамент"):
            cubix_page.navigation.find_and_click_available_apartment()

        with allure.step("Кликаем на кнопку Sales Offer"):
            cubix_page.click_sales_offer_button()

        with allure.step("Скачиваем PDF"):
            success, file_path = cubix_page.download_pdf_and_verify()
            cubix_page.assertions.assert_that(success, "PDF не был скачан")
            downloaded_file_path = file_path

        with allure.step("Проверяем что файл является валидным PDF"):
            with open(file_path, "rb") as f:
                content = f.read(10)
                cubix_page.assertions.assert_that(
                    content.startswith(b"%PDF"),
                    f"Файл не является валидным PDF, заголовок: {content[:10]}",
                )

    finally:
        # Очищаем скачанный файл в любом случае (успех или ошибка)
        if downloaded_file_path:
            with allure.step("Удаляем скачанный PDF файл"):
                cubix_page.cleanup_pdf_after_test()
