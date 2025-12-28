import allure
import pytest


@allure.feature("Abra - Проект Willows Residences")
@allure.story("View Brochures")
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.ui
def test_willows_residences_view_brochures(willows_residences_page):
    """Тест View Brochures для проекта Willows Residences - проверка открытия Google таблицы."""
    with allure.step("Открываем карту Abra"):
        willows_residences_page.open(route_type="map")

    with allure.step("Кликаем на проект Willows Residences"):
        willows_residences_page.map.navigate_to_project("willows_residences")

    with allure.step("Проверяем наличие кнопки View Brochures"):
        # Ищем кнопку View Brochures (для desktop используем второй элемент, индекс 1)
        view_brochures_button = willows_residences_page.page.locator(
            willows_residences_page.project_locators.VIEW_BROCHURES_BUTTON
        ).nth(1)

        view_brochures_button.wait_for(state="visible", timeout=10000)
        assert (
            view_brochures_button.is_visible()
        ), "Кнопка View Brochures не отображается"

        text = view_brochures_button.text_content()
        assert (
            "View Brochures" in text or "view brochures" in text.lower()
        ), f"Кнопка не содержит 'View Brochures': {text}"

        allure.attach(
            f"Найдена кнопка View Brochures\nТекст: {text}",
            name="View Brochures Button",
        )

    with allure.step(
        "Кликаем на кнопку View Brochures и проверяем открытие новой вкладки"
    ):
        # Получаем контекст браузера для работы с вкладками
        context = willows_residences_page.page.context

        # Ожидаем открытия новой вкладки
        with context.expect_page() as new_page_info:
            view_brochures_button.click()

        new_page = new_page_info.value
        new_page.wait_for_load_state("domcontentloaded")
        new_page.wait_for_timeout(3000)  # Ждем загрузки страницы

        # Проверяем URL новой вкладки
        new_page_url = new_page.url
        allure.attach(f"URL открытой страницы: {new_page_url}", name="Opened URL")

        # Проверяем, что это Google Drive/таблица
        assert (
            "google.com" in new_page_url
            or "drive.google.com" in new_page_url
            or "docs.google.com" in new_page_url
            or "sheets.google.com" in new_page_url
        ), f"Открыта не Google таблица/Drive. URL: {new_page_url}"

        with allure.step("Закрываем новую вкладку"):
            new_page.close()
