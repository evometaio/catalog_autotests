import os

import allure
import pytest


@allure.feature("Qube - Проект Arisha")
@allure.story("Тестовый кастомный POI")
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.ui
@pytest.mark.flaky(reruns=2, reruns_delay=4)
@pytest.mark.skipif(
    os.getenv("OS_PLATFORM") == "ubuntu-latest",
    reason="Тест нестабилен на Firefox в CI",
)
def test_arisha_map_poi(arisha_page):
    """Тест кастомного POI на карте"""

    with allure.step("Открываем карту и переходим к проекту Arisha"):
        arisha_page.open(route_type="map")
        arisha_page.map.navigate_to_project("arisha")

    with allure.step("Кликаем на кнопку All units"):
        arisha_page.click_all_units_button()
        arisha_page.assertions.assert_url_contains("catalog_2d", "Не перешли на страницу каталога")

    with allure.step("Ищем и кликаем на первый доступный апартамент"):
        arisha_page.navigation.find_and_click_available_apartment("arisha")

    with allure.step("Ожидаем полной загрузки виджета апартамента"):
        arisha_page.apartment_widget.wait_for_widget_load()

    with allure.step("Кликаем на кнопку 2D"):
        arisha_page.apartment_widget.switch_to_2d_mode()
        arisha_page.page.wait_for_timeout(1000)

    with allure.step("Проверяем появление навигации в режиме 2D"):
        arrows_visible = arisha_page.apartment_widget.check_navigation_arrows_visible()
        arisha_page.assertions.assert_that(
            arrows_visible, "Стрелочки навигации не появились в режиме 2D"
        )
        arisha_page.page.wait_for_timeout(1000)

    with allure.step("Кликаем на стрелочки для просмотра слайдов"):
        initial_scene = arisha_page.apartment_widget.get_current_scene()
        if initial_scene:
            allure.attach(
                f"Начальная сцена: {initial_scene}",
                name="Initial Scene",
                attachment_type=allure.attachment_type.TEXT,
            )

        # Просматриваем несколько слайдов
        scenes = arisha_page.apartment_widget.navigate_to_next_slide(3)

        for i, scene in enumerate(scenes):
            if scene:
                allure.attach(
                    f"Слайд #{i+1}: {scene}",
                    name=f"Slide {i+1}",
                    attachment_type=allure.attachment_type.TEXT,
                )

        arisha_page.page.wait_for_timeout(1000)

    with allure.step("Кликаем на кнопку 3D"):
        arisha_page.apartment_widget.switch_to_3d_mode()
        arisha_page.page.wait_for_timeout(1000)

        # Проверяем, что кнопка 3D стала активной
        button_active = arisha_page.apartment_widget.check_mode_button_active("3D")
        arisha_page.assertions.assert_that(button_active, "Кнопка 3D не стала активной")

    with allure.step("Кликаем на кнопку 0.5x"):
        speed_clicked = arisha_page.apartment_widget.click_speed_button()

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
        screenshot = arisha_page.apartment_widget.take_widget_screenshot()
        allure.attach(
            screenshot,
            name="Final Widget State",
            attachment_type=allure.attachment_type.PNG,
        )
