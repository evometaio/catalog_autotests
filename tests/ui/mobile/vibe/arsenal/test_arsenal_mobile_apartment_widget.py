import allure
import pytest


@allure.feature("Vibe - Проект Arsenal (mobile)")
@allure.story("Виджет апартамента")
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.mobile
def test_arsenal_mobile_apartment_widget_full_functionality(mobile_page):
    """Тест полного функционала виджета апартамента Arsenal на мобильном устройстве."""
    with allure.step("Открываем страницу map"):
        mobile_page.open(route_type="map")

    with allure.step("Кликаем на проект Arsenal на карте"):
        mobile_page.mobile_map.click_project("arsenal")

    with allure.step("Кликаем на Explore Project"):
        mobile_page.mobile_map.click_explore_project("arsenal")

    with allure.step("Ищем и кликаем на первый доступный апартамент"):
        mobile_page.mobile_navigation.find_and_click_available_apartment()
        mobile_page.page.wait_for_timeout(1000)

    with allure.step("Ожидаем полной загрузки виджета апартамента"):
        mobile_page.apartment_widget.wait_for_widget_load()

    with allure.step("Кликаем на кнопку 2D"):
        mobile_page.apartment_widget.switch_to_2d_mode()
        mobile_page.page.wait_for_timeout(1000)

        # Проверяем, что кнопка 2D стала активной
        button_active = mobile_page.apartment_widget.check_mode_button_active("2D")
        mobile_page.assertions.assert_that(
            button_active, "Кнопка 2D не стала активной (mobile)"
        )

    with allure.step("Кликаем на кнопку 3D"):
        mobile_page.apartment_widget.switch_to_3d_mode()
        mobile_page.page.wait_for_timeout(1000)

        # Проверяем, что кнопка 3D стала активной
        button_active = mobile_page.apartment_widget.check_mode_button_active("3D")
        mobile_page.assertions.assert_that(
            button_active, "Кнопка 3D не стала активной (mobile)"
        )

    with allure.step("Кликаем на кнопку зума 0.5x"):
        zoom_clicked = mobile_page.apartment_widget.click_zoom_button()

        if zoom_clicked:
            allure.attach(
                "Кликнули на кнопку зума 0.5x (mobile)",
                name="Zoom Control (mobile)",
                attachment_type=allure.attachment_type.TEXT,
            )
        else:
            allure.attach(
                "Кнопка зума 0.5x не найдена или не видима (mobile)",
                name="Zoom Control (mobile)",
                attachment_type=allure.attachment_type.TEXT,
            )

    with allure.step("Проверяем появление навигации в режиме 3D"):
        arrows_visible = mobile_page.apartment_widget.check_navigation_arrows_visible()
        mobile_page.assertions.assert_that(
            arrows_visible, "Стрелочки навигации не появились в режиме 3D (mobile)"
        )
        mobile_page.page.wait_for_timeout(1000)

    with allure.step("Кликаем на стрелочки для просмотра слайдов"):
        initial_scene = mobile_page.apartment_widget.get_current_scene()
        if initial_scene:
            allure.attach(
                f"Начальная сцена: {initial_scene}",
                name="Initial Scene (mobile)",
                attachment_type=allure.attachment_type.TEXT,
            )

        scenes = mobile_page.apartment_widget.navigate_to_next_slide(3)

        for i, scene in enumerate(scenes):
            if scene:
                allure.attach(
                    f"Слайд #{i+1}: {scene}",
                    name=f"Slide {i+1} (mobile)",
                    attachment_type=allure.attachment_type.TEXT,
                )

        mobile_page.page.wait_for_timeout(1000)

    with allure.step("Делаем скриншот финального состояния (mobile)"):
        screenshot = mobile_page.apartment_widget.take_widget_screenshot()
        allure.attach(
            screenshot,
            name="Final Widget State (mobile)",
            attachment_type=allure.attachment_type.PNG,
        )

    with allure.step("Проверяем адаптивность на мобильном устройстве"):
        mobile_page.check_mobile_viewport_adaptation()
