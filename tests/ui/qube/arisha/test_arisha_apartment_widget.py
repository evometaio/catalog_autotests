import os

import allure
import pytest


@allure.feature("Qube - Проект Arisha")
@allure.story("Виджет апартамента - Полный функционал")
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.ui
@pytest.mark.flaky(reruns=2, reruns_delay=4)
def test_arisha_apartment_widget_full_functionality(map_page):
    """Тест полного функционала виджета апартамента Arisha."""

    with allure.step("Открываем карту и переходим к проекту Arisha"):
        map_page.open(route_type="map")
        map_page.click_project_on_map("arisha")

    with allure.step("Кликаем на кнопку All units"):
        map_page.project.click_on_all_units_button()
        map_page.assert_url_contains("catalog_2d", "Не перешли на страницу каталога")

    with allure.step("Ищем и кликаем на первый доступный апартамент"):
        map_page.project.find_and_click_available_apartment("arisha")

    with allure.step("Ожидаем полной загрузки виджета апартамента"):
        # Ждем появления iframe
        map_page.page.wait_for_selector("iframe[class*='_iframe_']", timeout=15000)
        
        # Ждем загрузки содержимого внутри iframe
        frame_locator = map_page.apartment_widget.get_widget_frame()
        frame_locator.locator("body").wait_for(state="visible", timeout=15000)
        
        # Ждем появления кнопок режимов внутри виджета
        widget_locators = map_page.project_locators.Arisha.ApartmentWidget()
        view_2d_button = frame_locator.locator(widget_locators.VIEW_2D_BUTTON)
        view_3d_button = frame_locator.locator(widget_locators.VIEW_3D_BUTTON)
        
        view_2d_button.wait_for(state="visible", timeout=15000)
        view_3d_button.wait_for(state="visible", timeout=15000)

    with allure.step("Кликаем на кнопку 2D"):
        map_page.apartment_widget.switch_to_2d_mode("arisha")
        map_page.page.wait_for_timeout(500)

    with allure.step("Проверяем появление навигации в режиме 2D"):
        arrows_visible = map_page.apartment_widget.check_navigation_arrows_visible("arisha")
        map_page.assert_that(arrows_visible, "Стрелочки навигации не появились в режиме 2D")

    with allure.step("Кликаем на стрелочки для просмотра слайдов"):
        initial_scene = map_page.apartment_widget.get_current_scene("arisha")
        if initial_scene:
            allure.attach(
                f"Начальная сцена: {initial_scene}",
                name="Initial Scene",
                attachment_type=allure.attachment_type.TEXT,
            )

        # Просматриваем несколько слайдов
        scenes = map_page.apartment_widget.navigate_to_next_slide("arisha", 3)

        for i, scene in enumerate(scenes):
            if scene:
                allure.attach(
                    f"Слайд #{i+1}: {scene}",
                    name=f"Slide {i+1}",
                    attachment_type=allure.attachment_type.TEXT,
                )

        map_page.page.wait_for_timeout(500)

    with allure.step("Кликаем на кнопку 3D"):
        map_page.apartment_widget.switch_to_3d_mode("arisha")
        map_page.page.wait_for_timeout(500)

        # Проверяем, что кнопка 3D стала активной
        button_active = map_page.apartment_widget.check_mode_button_active("arisha", "3D")
        map_page.assert_that(button_active, "Кнопка 3D не стала активной")

    with allure.step("Кликаем на кнопку 0.5x"):
        speed_clicked = map_page.apartment_widget.click_speed_button("arisha")

        if speed_clicked:
            allure.attach(
                "Кликнули на кнопку скорости 0.5x",
                name="Speed Control",
                attachment_type=allure.attachment_type.TEXT,
            )
        else:
            allure.attach(
                "Кнопка скорости 0.5x не найдена или не видима",
                name="Speed Control",
                attachment_type=allure.attachment_type.TEXT,
            )

    with allure.step("Делаем скриншот финального состояния"):
        screenshot = map_page.apartment_widget.take_widget_screenshot()
        allure.attach(
            screenshot,
            name="Final Widget State",
            attachment_type=allure.attachment_type.PNG,
        )


@allure.feature("Qube - Проект Arisha")
@allure.story("Информация об апартаменте")
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.ui
@pytest.mark.flaky(reruns=2, reruns_delay=4)
def test_arisha_apartment_information(map_page):
    """Тест проверки информации об апартаменте Arisha."""

    with allure.step("Открываем карту и переходим к проекту Arisha"):
        map_page.open(route_type="map")
        map_page.click_project_on_map("arisha")

    with allure.step("Кликаем на кнопку All units"):
        map_page.project.click_on_all_units_button()
        map_page.assert_url_contains("catalog_2d", "Не перешли на страницу каталога")

    with allure.step("Ищем и кликаем на первый доступный апартамент"):
        map_page.project.find_and_click_available_apartment("arisha")

    with allure.step("Ожидаем полной загрузки страницы апартамента"):
        map_page.apartment_info.wait_for_info_to_appear("arisha")
        map_page.wait_for_timeout(2000)

    with allure.step("Проверяем тип апартамента"):
        type_visible = map_page.apartment_info.check_apartment_type("arisha")
        map_page.assert_that(type_visible, "Тип апартамента не отображается")

    with allure.step("Проверяем информацию о здании"):
        building_visible = map_page.apartment_info.check_building_info("arisha")
        map_page.assert_that(building_visible, "Информация о здании не найдена")

    with allure.step("Проверяем информацию о площади"):
        area_visible = map_page.apartment_info.check_area_info("arisha")
        map_page.assert_that(area_visible, "Информация о площади не найдена")

    with allure.step("Проверяем информацию о виде"):
        view_visible = map_page.apartment_info.check_view_info("arisha")
        map_page.assert_that(view_visible, "Информация о виде не найдена")

    with allure.step("Проверяем особенности апартамента"):
        features = map_page.apartment_info.check_features("arisha")

        map_page.assert_that(
            features["modern_design"], 
            "Особенность 'Modern interior design' не найдена"
        )
        map_page.assert_that(
            features["high_quality"], 
            "Особенность 'High quality materials' не найдена"
        )
        map_page.assert_that(
            features["built_in_appliances"], 
            "Особенность 'Built-in appliances' не найдена"
        )

    with allure.step("Проверяем счетчик просмотров"):
        watching_visible = map_page.apartment_info.check_watching_count("arisha")
        map_page.assert_that(watching_visible, "Счетчик просмотров 'watching now' не найден")

    with allure.step("Получаем полный текст информации"):
        info_text = map_page.apartment_info.get_info_text("arisha")
        allure.attach(info_text, name="Full Info Text", attachment_type=allure.attachment_type.TEXT)

        # Проверяем наличие ключевых элементов в тексте
        required_elements = [
            "APT.",
            "Bedroom",
            "Building:",
            "Total area:",
            "Modern interior design",
            "High quality materials",
            "Built-in appliances",
            "watching now",
        ]

        for element in required_elements:
            map_page.assert_that(
                element in info_text,
                f"Элемент '{element}' не найден в тексте информации об апартаменте"
            )

    with allure.step("Делаем скриншот информации об апартаменте"):
        info_screenshot = map_page.apartment_info.take_info_screenshot("arisha")
        allure.attach(
            info_screenshot,
            name="Apartment Info Screenshot",
            attachment_type=allure.attachment_type.PNG,
        )
