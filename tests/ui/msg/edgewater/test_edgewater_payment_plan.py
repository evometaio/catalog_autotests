import allure
import pytest


@allure.feature("MSG - Проект Edgewater")
@allure.story("Payment Plan")
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.ui
def test_edgewater_payment_plan(edgewater_page):
    """Тест Payment Plan для проекта Edgewater."""
    with allure.step("Открываем карту MSG"):
        edgewater_page.open(route_type="map")

    with allure.step("Кликаем на проект Edgewater"):
        edgewater_page.map.navigate_to_project("edgewater")

    with allure.step("Проверяем наличие кнопки Payment Plan"):
        # Для desktop используем второй элемент (индекс 1)
        payment_plan_button = edgewater_page.page.locator(
            edgewater_page.project_locators.PAYMENT_PLAN_BUTTON
        ).nth(1)
        payment_plan_button.wait_for(state="visible", timeout=10000)
        assert payment_plan_button.is_visible(), "Кнопка Payment Plan не отображается"

    with allure.step("Кликаем на кнопку Payment Plan"):
        payment_plan_button.click()

    with allure.step("Проверяем отображение модального окна Payment Plan"):
        modal = edgewater_page.page.locator(
            edgewater_page.project_locators.PAYMENT_PLAN_MODAL
        )
        modal.wait_for(state="visible", timeout=10000)
        assert modal.is_visible(), "Модальное окно Payment Plan не отображается"

    with allure.step("Проверяем наличие таблицы в модальном окне"):
        table = edgewater_page.page.locator(
            edgewater_page.project_locators.PAYMENT_PLAN_TABLE
        )
        table.wait_for(state="visible", timeout=10000)
        assert table.is_visible(), "Таблица не отображается в модальном окне"

    with allure.step("Проверяем заголовки таблицы"):
        headers = table.locator("th, .ant-table-thead th")
        header_count = headers.count()
        assert (
            header_count >= 3
        ), f"Ожидалось минимум 3 заголовка, найдено: {header_count}"

        # Проверяем наличие ожидаемых заголовков
        header_texts = [headers.nth(i).text_content() for i in range(header_count)]
        allure.attach(
            f"Заголовки таблицы: {', '.join(header_texts)}", name="Table Headers"
        )

        assert "Installment" in " ".join(
            header_texts
        ), "Заголовок 'Installment' не найден"
        assert "Percentage" in " ".join(
            header_texts
        ), "Заголовок 'Percentage' не найден"
        assert "Payment Date" in " ".join(
            header_texts
        ), "Заголовок 'Payment Date' не найден"

    with allure.step("Проверяем наличие строк в таблице"):
        rows = table.locator("tr, .ant-table-row")
        row_count = rows.count()
        assert row_count > 0, "Таблица не содержит строк"
        allure.attach(
            f"Количество строк в таблице: {row_count}", name="Table Rows Count"
        )

    with allure.step("Проверяем наличие кнопки закрытия модального окна"):
        close_button = edgewater_page.page.locator(
            edgewater_page.project_locators.PAYMENT_PLAN_MODAL_CLOSE
        )
        assert close_button.is_visible(), "Кнопка закрытия не отображается"

    with allure.step("Закрываем модальное окно Payment Plan"):
        close_button.click()
        modal.wait_for(state="hidden", timeout=5000)

    with allure.step("Проверяем, что модальное окно закрылось"):
        assert not modal.is_visible(), "Модальное окно не закрылось"
