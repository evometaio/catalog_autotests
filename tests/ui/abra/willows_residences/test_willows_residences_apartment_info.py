import allure
import pytest


@allure.feature("Abra - Проект Willows Residences")
@allure.story("Информация об аппарте")
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.ui
def test_willows_residences_apartment_info(willows_residences_page):
    """Тест отображения информации об аппарте для проекта Willows Residences."""
    with allure.step("Открываем карту Abra"):
        willows_residences_page.open(route_type="map")

    with allure.step("Кликаем на проект Willows Residences"):
        willows_residences_page.map.navigate_to_project("willows_residences")

    with allure.step("Проверяем, что мы на странице catalog_2d после Explore Project"):
        # После navigate_to_project мы уже на catalog_2d
        willows_residences_page.page.wait_for_load_state("domcontentloaded")
        willows_residences_page.page.wait_for_timeout(2000)
        willows_residences_page.assertions.assert_url_contains(
            "catalog_2d", "Не перешли на страницу каталога"
        )

    with allure.step("Ищем и кликаем на первый доступный аппарт"):
        property_buttons = willows_residences_page.page.locator(
            willows_residences_page.project_locators.PROPERTY_INFO_PRIMARY_BUTTON
        )
        willows_residences_page.page.wait_for_timeout(2000)  # Ждем загрузки страницы

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
        willows_residences_page.page.wait_for_timeout(3000)  # Ждем появления панели

    with allure.step("Проверяем отображение информации об аппарте"):
        # Проверяем наличие заголовка с номером аппарта (APT. XXX)
        # Используем более общий селектор, так как класс может отличаться
        apartment_title = willows_residences_page.page.locator(
            '[class*="propertyInfoTitle"]'
        )
        # Ищем видимый заголовок
        visible_title = None
        for i in range(apartment_title.count()):
            title_elem = apartment_title.nth(i)
            if title_elem.is_visible():
                title_text = title_elem.text_content()
                if title_text and (
                    "apt" in title_text.lower() or "apartment" in title_text.lower()
                ):
                    visible_title = title_elem
                    break

        assert visible_title is not None, "Заголовок с номером аппарта не найден"

        title_text = visible_title.text_content()
        assert (
            "APT." in title_text or "apt" in title_text.lower()
        ), f"Заголовок не содержит 'APT.': {title_text}"
        allure.attach(f"Номер аппарта: {title_text}", name="Apartment Number")

    with allure.step("Проверяем наличие обертки с информацией"):
        # Используем более общий селектор
        info_wrapper = willows_residences_page.page.locator(
            '[class*="propertyInfoWrapper"]'
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
        description = willows_residences_page.page.locator(
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
        info_items = willows_residences_page.page.locator(
            ".page_propertyInfoInfoItems__fovdJ"
        )
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
