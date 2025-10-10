import allure
import pytest


@allure.feature("Qube - Проект Arisha (mobile)")
@allure.story("Виджет апартамента - Мобильная")
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.mobile
@pytest.mark.skip(reason="Реализовать")
def test_arisha_mobile_apartment_widget_full_functionality(mobile_page):
    """Тест полного функционала виджета апартамента Arisha на мобильном устройстве."""

    with allure.step("Открываем карту и переходим к проекту Arisha"):
        mobile_page.open(route_type="map")
        mobile_page.click_mobile_project_on_map("arisha")

    with allure.step("Кликаем на Explore Project"):
        mobile_page.click_mobile_explore_project_button("arisha")

    with allure.step("Ищем и кликаем на первый доступный апартамент"):
        mobile_page.find_and_click_available_apartment()

    with allure.step("Ожидаем полной загрузки виджета апартамента"):
        # Ждем появления iframe
        mobile_page.page.wait_for_selector("iframe[class*='_iframe_']", timeout=15000)

        # Ждем загрузки содержимого внутри iframe
        mobile_page.page.wait_for_timeout(4000)

    with allure.step("Кликаем на кнопку 2D"):
        mobile_page.apartment_widget.switch_to_2d_mode("arisha")
        mobile_page.page.wait_for_timeout(1000)

    with allure.step("Проверяем появление навигации в режиме 2D"):
        arrows_visible = mobile_page.apartment_widget.check_navigation_arrows_visible(
            "arisha"
        )
        mobile_page.assert_that(
            arrows_visible, "Стрелочки навигации не появились в режиме 2D"
        )
        mobile_page.page.wait_for_timeout(1000)

    with allure.step("Кликаем на стрелочки для просмотра слайдов"):
        initial_scene = mobile_page.apartment_widget.get_current_scene("arisha")
        if initial_scene:
            allure.attach(
                f"Начальная сцена: {initial_scene}",
                name="Initial Scene",
                attachment_type=allure.attachment_type.TEXT,
            )

        # Просматриваем несколько слайдов
        scenes = mobile_page.apartment_widget.navigate_to_next_slide("arisha", 3)

        for i, scene in enumerate(scenes):
            if scene:
                allure.attach(
                    f"Слайд #{i+1}: {scene}",
                    name=f"Slide {i+1}",
                    attachment_type=allure.attachment_type.TEXT,
                )

        mobile_page.page.wait_for_timeout(1000)

    with allure.step("Кликаем на кнопку 3D"):
        mobile_page.apartment_widget.switch_to_3d_mode("arisha")
        mobile_page.page.wait_for_timeout(1000)

        # Проверяем, что кнопка 3D стала активной
        button_active = mobile_page.apartment_widget.check_mode_button_active(
            "arisha", "3D"
        )
        mobile_page.assert_that(button_active, "Кнопка 3D не стала активной")

    with allure.step("Делаем скриншот финального состояния"):
        screenshot = mobile_page.apartment_widget.take_widget_screenshot()
        allure.attach(
            screenshot,
            name="Final Widget State",
            attachment_type=allure.attachment_type.PNG,
        )

    with allure.step("Проверяем адаптивность на мобильном устройстве"):
        mobile_page.check_mobile_viewport_adaptation()


@allure.feature("Qube - Проект Arisha (mobile)")
@allure.story("Информация об апартаменте - Мобильная")
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.mobile
@pytest.mark.skip(reason="Реализовать")
def test_arisha_mobile_apartment_information(mobile_page):
    """Тест проверки информации об апартаменте Arisha на мобильном устройстве."""

    with allure.step("Открываем карту и переходим к проекту Arisha"):
        mobile_page.open(route_type="map")
        mobile_page.click_mobile_project_on_map("arisha")

    with allure.step("Кликаем на Explore Project"):
        mobile_page.click_mobile_explore_project_button("arisha")

    with allure.step("Ищем и кликаем на первый доступный апартамент"):
        mobile_page.find_and_click_available_apartment()

    with allure.step("Ожидаем полной загрузки страницы апартамента"):
        mobile_page.apartment_info.wait_for_info_to_appear("arisha")
        mobile_page.wait_for_timeout(2000)

    with allure.step("Проверяем тип апартамента"):
        type_visible = mobile_page.apartment_info.check_apartment_type("arisha")
        mobile_page.assert_that(type_visible, "Тип апартамента не отображается")

    with allure.step("Проверяем информацию о здании"):
        building_visible = mobile_page.apartment_info.check_building_info("arisha")
        mobile_page.assert_that(building_visible, "Информация о здании не найдена")

    with allure.step("Проверяем информацию о площади"):
        area_visible = mobile_page.apartment_info.check_area_info("arisha")
        mobile_page.assert_that(area_visible, "Информация о площади не найдена")

    with allure.step("Проверяем информацию о виде"):
        view_visible = mobile_page.apartment_info.check_view_info("arisha")
        mobile_page.assert_that(view_visible, "Информация о виде не найдена")

    with allure.step("Проверяем особенности апартамента"):
        features = mobile_page.apartment_info.check_features("arisha")

        mobile_page.assert_that(
            features["modern_design"], "Особенность 'Modern interior design' не найдена"
        )
        mobile_page.assert_that(
            features["high_quality"], "Особенность 'High quality materials' не найдена"
        )
        mobile_page.assert_that(
            features["built_in_appliances"],
            "Особенность 'Built-in appliances' не найдена",
        )

    with allure.step("Проверяем счетчик просмотров"):
        watching_visible = mobile_page.apartment_info.check_watching_count("arisha")
        mobile_page.assert_that(
            watching_visible, "Счетчик просмотров 'watching now' не найден"
        )

    with allure.step("Получаем полный текст информации"):
        info_text = mobile_page.apartment_info.get_info_text("arisha")
        allure.attach(
            info_text,
            name="Full Info Text",
            attachment_type=allure.attachment_type.TEXT,
        )

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
            mobile_page.assert_that(
                element in info_text,
                f"Элемент '{element}' не найден в тексте информации об апартаменте",
            )

    with allure.step("Делаем скриншот информации об апартаменте"):
        info_screenshot = mobile_page.apartment_info.take_info_screenshot("arisha")
        allure.attach(
            info_screenshot,
            name="Apartment Info Screenshot",
            attachment_type=allure.attachment_type.PNG,
        )

    with allure.step("Проверяем адаптивность на мобильном устройстве"):
        mobile_page.check_mobile_viewport_adaptation()
