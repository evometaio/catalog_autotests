import os

import allure
import pytest


@allure.feature("Vibe - Проект Arsenal")
@allure.story("Виджет апартамента - Полный функционал")
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.ui
@pytest.mark.skipif(
    os.getenv("TEST_ENVIRONMENT", "prod") != "dev",
    reason="Тест запускается только на dev окружении",
)
def test_arsenal_apartment_widget_full_functionality(arsenal_page):
    """Тест полного функционала виджета апартамента Arsenal."""
    with allure.step("Открываем страницу map"):
        arsenal_page.open(route_type="map")

    with allure.step("Кликаем на кнопку All units"):
        arsenal_page.click_all_units_button()
        arsenal_page.assertions.assert_url_contains(
            "catalog_2d", "Не перешли на страницу каталога"
        )

    with allure.step("Ищем и кликаем на первый доступный апартамент"):
        arsenal_page.navigation.find_and_click_available_apartment(
            project_name="arsenal"
        )

    with allure.step("Ожидаем полной загрузки виджета апартамента"):
        arsenal_page.apartment_widget.wait_for_widget_load()

    with allure.step("Кликаем на кнопку 2D"):
        arsenal_page.apartment_widget.switch_to_2d_mode()
        arsenal_page.page.wait_for_timeout(1000)

        # Проверяем, что кнопка 2D стала активной
        button_active = arsenal_page.apartment_widget.check_mode_button_active("2D")
        arsenal_page.assertions.assert_that(
            button_active, "Кнопка 2D не стала активной"
        )

    with allure.step("Кликаем на кнопку 3D"):
        arsenal_page.apartment_widget.switch_to_3d_mode()
        arsenal_page.page.wait_for_timeout(1000)

        # Проверяем, что кнопка 3D стала активной
        button_active = arsenal_page.apartment_widget.check_mode_button_active("3D")
        arsenal_page.assertions.assert_that(
            button_active, "Кнопка 3D не стала активной"
        )

    with allure.step("Кликаем на кнопку зума 0.5x"):
        zoom_clicked = arsenal_page.apartment_widget.click_zoom_button()

        if zoom_clicked:
            allure.attach(
                "Кликнули на кнопку зума 0.5x",
                name="Zoom Control",
                attachment_type=allure.attachment_type.TEXT,
            )
        else:
            allure.attach(
                "Кнопка зума 0.5x не найдена или не видима",
                name="Zoom Control",
                attachment_type=allure.attachment_type.TEXT,
            )

    with allure.step("Проверяем появление навигации в режиме 3D"):
        arrows_visible = arsenal_page.apartment_widget.check_navigation_arrows_visible()
        arsenal_page.assertions.assert_that(
            arrows_visible, "Стрелочки навигации не появились в режиме 3D"
        )
        arsenal_page.page.wait_for_timeout(1000)

    with allure.step("Кликаем на стрелочки для просмотра слайдов"):
        initial_scene = arsenal_page.apartment_widget.get_current_scene()
        if initial_scene:
            allure.attach(
                f"Начальная сцена: {initial_scene}",
                name="Initial Scene",
                attachment_type=allure.attachment_type.TEXT,
            )

        # Просматриваем несколько слайдов
        scenes = arsenal_page.apartment_widget.navigate_to_next_slide(3)

        for i, scene in enumerate(scenes):
            if scene:
                allure.attach(
                    f"Слайд #{i+1}: {scene}",
                    name=f"Slide {i+1}",
                    attachment_type=allure.attachment_type.TEXT,
                )

        arsenal_page.page.wait_for_timeout(1000)

    with allure.step("Делаем скриншот финального состояния"):
        screenshot = arsenal_page.apartment_widget.take_widget_screenshot()
        allure.attach(
            screenshot,
            name="Final Widget State",
            attachment_type=allure.attachment_type.PNG,
        )
