import allure
import pytest


@allure.feature("MSG - Проект Edgewater")
@allure.story("Пагинация каталога")
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.ui
def test_edgewater_catalog_pagination(edgewater_page):
    """Тест пагинации каталога аппартов для проекта Edgewater."""
    with allure.step("Открываем карту MSG"):
        edgewater_page.open(route_type="map")

    with allure.step("Кликаем на проект Edgewater"):
        edgewater_page.map.navigate_to_project("edgewater")

    with allure.step("Проверяем, что мы на странице catalog_2d"):
        edgewater_page.page.wait_for_load_state("domcontentloaded")
        edgewater_page.page.wait_for_timeout(2000)
        edgewater_page.assertions.assert_url_contains(
            "catalog_2d", "Не перешли на страницу каталога"
        )

    with allure.step("Проверяем наличие кнопок аппартов на первой странице"):
        property_buttons_page1 = edgewater_page.page.locator(
            edgewater_page.project_locators.PROPERTY_INFO_PRIMARY_BUTTON
        )
        edgewater_page.page.wait_for_timeout(2000)  # Ждем загрузки страницы

        # Находим первую видимую кнопку
        first_visible_button_page1 = None
        for i in range(property_buttons_page1.count()):
            btn = property_buttons_page1.nth(i)
            if btn.is_visible():
                first_visible_button_page1 = btn
                break

        assert (
            first_visible_button_page1 is not None
        ), "Не найдено видимых кнопок аппартов на первой странице"

        count_page1 = property_buttons_page1.count()
        # Сохраняем ID первого видимого аппарта для сравнения
        first_apartment_id_page1 = first_visible_button_page1.get_attribute(
            "data-test-id"
        )
        allure.attach(
            f"Количество аппартов на странице 1: {count_page1}\nПервый аппарт: {first_apartment_id_page1}",
            name="Page 1 Info",
        )

    with allure.step("Проверяем наличие пагинации"):
        pagination_items = edgewater_page.page.locator(
            edgewater_page.project_locators.PAGINATION_ITEM
        )
        pagination_count = pagination_items.count()

        if pagination_count == 0:
            pytest.skip("Пагинация не найдена, возможно все аппарты на одной странице")

        allure.attach(
            f"Найдено элементов пагинации: {pagination_count}", name="Pagination Info"
        )

    with allure.step("Кликаем на страницу 2 пагинации"):
        # Ищем кнопку страницы 2
        page_2_button = edgewater_page.page.locator(
            'li.ant-pagination-item-2, li[title="2"]'
        )

        if page_2_button.count() == 0:
            pytest.skip("Кнопка страницы 2 не найдена")

        page_2_button.first.wait_for(state="visible", timeout=5000)
        assert page_2_button.first.is_visible(), "Кнопка страницы 2 не видна"

        page_2_button.first.click()
        edgewater_page.page.wait_for_timeout(3000)  # Ждем загрузки страницы 2

    with allure.step("Проверяем, что мы перешли на страницу 2"):
        # Проверяем, что кнопка страницы 2 активна
        active_page_2 = edgewater_page.page.locator(
            'li.ant-pagination-item-2.ant-pagination-item-active, li[title="2"].ant-pagination-item-active'
        )
        active_page_2.wait_for(state="visible", timeout=5000)
        assert active_page_2.is_visible(), "Страница 2 не стала активной"

    with allure.step("Проверяем наличие кнопок аппартов на второй странице"):
        property_buttons_page2 = edgewater_page.page.locator(
            edgewater_page.project_locators.PROPERTY_INFO_PRIMARY_BUTTON
        )

        # Находим первую видимую кнопку на странице 2
        first_visible_button_page2 = None
        for i in range(property_buttons_page2.count()):
            btn = property_buttons_page2.nth(i)
            if btn.is_visible():
                first_visible_button_page2 = btn
                break

        assert (
            first_visible_button_page2 is not None
        ), "Не найдено видимых кнопок аппартов на второй странице"

        count_page2 = property_buttons_page2.count()
        # Сохраняем ID первого видимого аппарта для сравнения
        first_apartment_id_page2 = first_visible_button_page2.get_attribute(
            "data-test-id"
        )
        allure.attach(
            f"Количество аппартов на странице 2: {count_page2}\nПервый аппарт: {first_apartment_id_page2}",
            name="Page 2 Info",
        )

    with allure.step("Проверяем, что на странице 2 отображаются другие аппарты"):
        # Проверяем, что первый аппарт на странице 2 отличается от первого на странице 1
        assert (
            first_apartment_id_page1 != first_apartment_id_page2
        ), f"На странице 2 отображается тот же аппарт, что и на странице 1: {first_apartment_id_page1}"
