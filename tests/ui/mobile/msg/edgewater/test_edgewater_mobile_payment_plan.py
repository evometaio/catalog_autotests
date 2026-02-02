import allure
import pytest


@allure.feature("MSG - Проект Edgewater (mobile)")
@allure.story("Payment Plan")
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.mobile
def test_edgewater_mobile_payment_plan(mobile_page):
    """Тест Payment Plan для проекта Edgewater на мобильном устройстве."""
    with allure.step("Открываем карту MSG"):
        mobile_page.open(route_type="map")

    with allure.step("Кликаем на проект Edgewater"):
        mobile_page.mobile_map.click_project("edgewater")

    with allure.step("Кликаем на Explore Project"):
        mobile_page.mobile_map.click_explore_project("edgewater")

    with allure.step("Открываем меню и переходим в All Units (catalog_2d)"):
        menu_button = mobile_page.page.locator(
            '[data-test-id="nav-mobile-menu-toggle"]'
        )
        menu_button.wait_for(state="visible", timeout=10000)
        menu_button.click()
        mobile_page.page.wait_for_timeout(1000)

        all_units_button = mobile_page.page.locator(
            '[data-test-id="nav-mobile-catalog2d"]'
        )
        all_units_button.wait_for(state="visible", timeout=10000)
        all_units_button.click()
        mobile_page.page.wait_for_url("**/catalog_2d", timeout=20000)

    with allure.step("Проверяем наличие кнопки Payment Plan"):
        # Для mobile используем первый элемент (индекс 0)
        payment_plan_button = mobile_page.page.locator(
            mobile_page.project_locators.PAYMENT_PLAN_BUTTON
        ).first
        payment_plan_button.wait_for(state="visible", timeout=10000)
        assert payment_plan_button.is_visible(), "Кнопка Payment Plan не отображается"

    with allure.step("Кликаем на кнопку Payment Plan"):
        payment_plan_button.click()
        mobile_page.page.wait_for_timeout(2000)  # Ждем появления модального окна

    with allure.step("Проверяем отображение модального окна Payment Plan"):
        # На мобильной версии используем более общий селектор
        modal = mobile_page.page.locator('.ant-modal-wrap, [role="dialog"]').first
        modal.wait_for(state="visible", timeout=15000)
        assert modal.is_visible(), "Модальное окно Payment Plan не отображается"

    with allure.step("Проверяем наличие таблицы в модальном окне"):
        table = mobile_page.page.locator(
            mobile_page.project_locators.PAYMENT_PLAN_TABLE
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
        close_button = mobile_page.page.locator(
            mobile_page.project_locators.PAYMENT_PLAN_MODAL_CLOSE
        ).first
        assert close_button.is_visible(), "Кнопка закрытия не отображается"

    with allure.step("Закрываем модальное окно Payment Plan"):
        close_button.click()
        mobile_page.page.wait_for_timeout(1000)
        modal.wait_for(state="hidden", timeout=5000)

    with allure.step("Проверяем, что модальное окно закрылось"):
        assert not modal.is_visible(), "Модальное окно не закрылось"

    with allure.step("Проверяем адаптивность на мобильном устройстве"):
        mobile_page.check_mobile_viewport_adaptation()
