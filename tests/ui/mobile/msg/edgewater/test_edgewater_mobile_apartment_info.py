import allure
import pytest


@allure.feature("MSG - Проект Edgewater (mobile)")
@allure.story("Информация об аппарте")
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.mobile
def test_edgewater_mobile_apartment_info(mobile_page):
    """Тест отображения информации об аппарте для проекта Edgewater на мобильном устройстве."""
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
        menu_button.wait_for(state="visible", timeout=20000)
        menu_button.click()
        mobile_page.page.wait_for_timeout(1000)

        all_units_button = mobile_page.page.locator(
            '[data-test-id="nav-mobile-catalog2d"]'
        )
        all_units_button.wait_for(state="visible", timeout=20000)
        all_units_button.click()
        mobile_page.page.wait_for_url("**/catalog_2d", timeout=20000)

    with allure.step("Проверяем, что мы на странице catalog_2d"):
        mobile_page.page.wait_for_load_state("domcontentloaded")
        mobile_page.page.wait_for_timeout(2000)
        assert "catalog_2d" in mobile_page.page.url, "Не перешли на страницу каталога"

    with allure.step("Ищем и кликаем на первый доступный аппарт"):
        property_buttons = mobile_page.page.locator(
            mobile_page.project_locators.PROPERTY_INFO_PRIMARY_BUTTON
        )
        property_buttons.first.wait_for(state="visible", timeout=20000)

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
        mobile_page.page.wait_for_timeout(3000)  # Ждем появления панели

    with allure.step("Проверяем отображение информации об аппарте"):
        # Проверяем наличие заголовка с номером аппарта (APT. XXX)
        apartment_title = mobile_page.page.locator(
            mobile_page.project_locators.APARTMENT_INFO_TITLE
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
        info_wrapper = mobile_page.page.locator(
            mobile_page.project_locators.APARTMENT_INFO_WRAPPER
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
        description = mobile_page.page.locator(".page_propertyInfoDescription__E_EB7")
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
        info_items = mobile_page.page.locator(".page_propertyInfoInfoItems__fovdJ")
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

    with allure.step("Проверяем адаптивность на мобильном устройстве"):
        mobile_page.check_mobile_viewport_adaptation()
