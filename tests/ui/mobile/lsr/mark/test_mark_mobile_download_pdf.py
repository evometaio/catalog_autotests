import os

import allure
import pytest


@allure.feature("LSR - Проект MARK (mobile)")
@allure.story("Скачивание PDF предложения")
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.mobile
@pytest.mark.skipif(
    os.getenv("TEST_ENVIRONMENT", "prod") not in ["dev", "stage"],
    reason="Тест запускается только на dev и stage окружениях",
)
def test_mark_mobile_download_pdf(mark_page):
    """Тест скачивания PDF для проекта MARK на мобильном устройстве."""
    downloaded_file_path = ""

    try:
        with allure.step("Открываем главную страницу MARK (mobile)"):
            mark_page.open()

        with allure.step("Переходим в каталог через мобильное меню"):
            menu_toggle = mark_page.page.locator(
                mark_page.project_locators.NAV_MOBILE_MENU_TOGGLE
            )
            menu_toggle.wait_for(state="visible", timeout=10000)
            menu_toggle.click()

            catalog_button = mark_page.page.locator(
                mark_page.project_locators.NAV_MOBILE_CATALOG2D
            )
            catalog_button.wait_for(state="visible", timeout=10000)
            catalog_button.click()

        with allure.step("Ищем и кликаем на первый доступный апартамент"):
            mark_page.navigation.find_and_click_available_apartment(project_name="mark")

        with allure.step("Ожидаем полной загрузки виджета апартамента"):
            mark_page.apartment_widget.wait_for_widget_load()

        with allure.step("Скачиваем PDF"):
            success, file_path = mark_page.download_pdf_and_verify()
            mark_page.assertions.assert_that(success, "PDF не был скачан")
            downloaded_file_path = file_path

        with allure.step("Проверяем что файл является валидным PDF"):
            with open(file_path, "rb") as f:
                content = f.read(10)
                mark_page.assertions.assert_that(
                    content.startswith(b"%PDF"),
                    f"Файл не является валидным PDF, заголовок: {content[:10]}",
                )

    finally:
        if downloaded_file_path:
            with allure.step("Удаляем скачанный PDF файл"):
                mark_page.cleanup_pdf_after_test()
