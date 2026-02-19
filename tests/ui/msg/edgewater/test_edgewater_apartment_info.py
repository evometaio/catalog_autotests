import allure
import pytest


@allure.feature("MSG - Проект Edgewater")
@allure.story("Информация об аппарте")
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.ui
def test_edgewater_apartment_info(edgewater_page):
    """Тест отображения информации об аппарте для проекта Edgewater."""
    with allure.step("Открываем карту MSG"):
        edgewater_page.open(route_type="map")

    with allure.step("Кликаем на проект Edgewater"):
        edgewater_page.map.navigate_to_project("edgewater")

    with allure.step("Кликаем на кнопку All Units для перехода на catalog2d"):
        edgewater_page.browser.expect_visible(
            edgewater_page.project_locators.ALL_UNITS_BUTTON
        )
        edgewater_page.browser.click(edgewater_page.project_locators.ALL_UNITS_BUTTON)
        edgewater_page.page.wait_for_url("**/catalog_2d", timeout=20000)

    with allure.step("Проверяем, что мы на странице catalog_2d после Explore Project"):
        edgewater_page.page.wait_for_load_state("domcontentloaded")
        edgewater_page.page.wait_for_timeout(2000)
        edgewater_page.assertions.assert_url_contains(
            "catalog_2d", "Не перешли на страницу каталога"
        )

    with allure.step("Ищем и кликаем на первый доступный аппарт"):
        property_buttons = edgewater_page.page.locator(
            edgewater_page.project_locators.PROPERTY_INFO_PRIMARY_BUTTON
        )
        # Находим первую видимую кнопку
        visible_button = None
        for i in range(property_buttons.count()):
            btn = property_buttons.nth(i)
            if btn.is_visible():
                visible_button = btn
                test_id = btn.get_attribute("data-test-id")
                allure.attach(f"Кликаем на аппарт: {test_id}", name="Apartment Button")
                break

        assert visible_button is not None, "Не найдено видимых кнопок аппартов"
        visible_button.click()
        edgewater_page.page.wait_for_timeout(3000)  # Ждем появления панели

    with allure.step("Проверяем отображение информации об аппарте"):
        # Проверяем наличие заголовка с номером аппарта (APT. XXX)
        apartment_title = edgewater_page.page.locator(
            edgewater_page.project_locators.APARTMENT_INFO_TITLE
        )
        # Ищем видимый заголовок
        visible_title = None
        for i in range(apartment_title.count()):
            title_elem = apartment_title.nth(i)
            if title_elem.is_visible():
                visible_title = title_elem
                break

        assert visible_title is not None, "Заголовок с номером аппарта не найден"

        title_text = visible_title.text_content()
        assert "APT." in title_text, f"Заголовок не содержит 'APT.': {title_text}"
        allure.attach(f"Номер аппарта: {title_text}", name="Apartment Number")

    with allure.step("Проверяем наличие обертки с информацией"):
        info_wrapper = edgewater_page.page.locator(
            edgewater_page.project_locators.APARTMENT_INFO_WRAPPER
        )
        # Ищем видимую обертку
        visible_wrapper = None
        for i in range(info_wrapper.count()):
            wrapper_elem = info_wrapper.nth(i)
            if wrapper_elem.is_visible():
                visible_wrapper = wrapper_elem
                break

        assert visible_wrapper is not None, "Обертка с информацией не найдена"

    with allure.step("Проверяем наличие описания/информации об аппарте"):
        description = edgewater_page.page.locator(
            ".page_propertyInfoDescription__E_EB7"
        )
        if description.count() > 0:
            # Ищем видимое описание
            visible_desc = None
            for i in range(description.count()):
                desc_elem = description.nth(i)
                if desc_elem.is_visible():
                    visible_desc = desc_elem
                    break

            if visible_desc:
                desc_text = visible_desc.text_content()
                allure.attach(
                    f"Описание: {desc_text[:200] if desc_text else 'N/A'}",
                    name="Apartment Description",
                )

    with allure.step("Проверяем наличие информации о цене или других параметрах"):
        # Ищем элементы с информацией (цена, площадь и т.д.)
        info_items = edgewater_page.page.locator(".page_propertyInfoInfoItems__fovdJ")
        if info_items.count() > 0:
            # Ищем видимые информационные элементы
            visible_info = None
            for i in range(info_items.count()):
                info_elem = info_items.nth(i)
                if info_elem.is_visible():
                    visible_info = info_elem
                    break

            if visible_info:
                info_text = visible_info.text_content()
                allure.attach(
                    f"Информация: {info_text[:200] if info_text else 'N/A'}",
                    name="Apartment Info",
                )
