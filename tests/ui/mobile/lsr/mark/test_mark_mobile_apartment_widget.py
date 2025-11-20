import os

import allure
import pytest


@allure.feature("LSR - Проект MARK (mobile)")
@allure.story("Виджет апартамента")
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.mobile
@pytest.mark.skipif(
    os.getenv("TEST_ENVIRONMENT", "prod") != "dev",
    reason="Тест запускается только на dev окружении",
)
def test_mark_mobile_apartment_widget_full_functionality(mark_page):
    """Тест полного функционала виджета апартамента MARK на мобильном устройстве."""
    with allure.step("Открываем главную страницу MARK (mobile)"):
        mark_page.open()

    with allure.step("Переходим в каталог через мобильное меню"):
        menu_toggle = mark_page.page.locator(
            mark_page.project_locators.NAV_MOBILE_MENU_TOGGLE
        )
        menu_toggle.wait_for(state="visible", timeout=10000)
        menu_toggle.click()

        catalog_button = mark_page.page.locator(
            mark_page.project_locators.NAV_MOBILE_CATALOG2D
        )
        catalog_button.wait_for(state="visible", timeout=10000)
        catalog_button.click()

    with allure.step("Ищем и кликаем на первый доступный апартамент"):
        mark_page.navigation.find_and_click_available_apartment(project_name="mark")

    with allure.step("Ожидаем полной загрузки виджета апартамента"):
        mark_page.apartment_widget.wait_for_widget_load()

    with allure.step("Кликаем на кнопку 2D"):
        mark_page.apartment_widget.switch_to_2d_mode()
        mark_page.page.wait_for_timeout(1000)

        # Проверяем, что кнопка 2D стала активной
        button_active = mark_page.apartment_widget.check_mode_button_active("2D")
        mark_page.assertions.assert_that(
            button_active, "Кнопка 2D не стала активной (mobile)"
        )

    with allure.step("Кликаем на кнопку 3D"):
        mark_page.apartment_widget.switch_to_3d_mode()
        mark_page.page.wait_for_timeout(1000)

        # Проверяем, что кнопка 3D стала активной
        button_active = mark_page.apartment_widget.check_mode_button_active("3D")
        mark_page.assertions.assert_that(
            button_active, "Кнопка 3D не стала активной (mobile)"
        )

    with allure.step("Кликаем на кнопку зума 0.5x"):
        zoom_clicked = mark_page.apartment_widget.click_zoom_button()

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
        arrows_visible = mark_page.apartment_widget.check_navigation_arrows_visible()
        mark_page.assertions.assert_that(
            arrows_visible, "Стрелочки навигации не появились в режиме 3D (mobile)"
        )
        mark_page.page.wait_for_timeout(1000)

    with allure.step("Кликаем на стрелочки для просмотра слайдов"):
        initial_scene = mark_page.apartment_widget.get_current_scene()
        if initial_scene:
            allure.attach(
                f"Начальная сцена: {initial_scene}",
                name="Initial Scene (mobile)",
                attachment_type=allure.attachment_type.TEXT,
            )

        scenes = mark_page.apartment_widget.navigate_to_next_slide(3)

        for i, scene in enumerate(scenes):
            if scene:
                allure.attach(
                    f"Слайд #{i+1}: {scene}",
                    name=f"Slide {i+1} (mobile)",
                    attachment_type=allure.attachment_type.TEXT,
                )

        mark_page.page.wait_for_timeout(1000)

    with allure.step("Делаем скриншот финального состояния (mobile)"):
        screenshot = mark_page.apartment_widget.take_widget_screenshot()
        allure.attach(
            screenshot,
            name="Final Widget State (mobile)",
            attachment_type=allure.attachment_type.PNG,
        )
