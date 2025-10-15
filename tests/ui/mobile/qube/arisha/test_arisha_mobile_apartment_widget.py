import allure
import pytest


@allure.feature("Qube - Проект Arisha (mobile)")
@allure.story("Виджет апартамента - Мобильная")
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.mobile
@pytest.mark.parametrize("route_type", ["map", "agent", "client"])
def test_arisha_mobile_apartment_widget_full_functionality(mobile_page, route_type):
    """Тест полного функционала виджета апартамента Arisha на мобильном устройстве на всех роутах."""

    with allure.step(f"Открываем страницу {route_type} и переходим к проекту Arisha"):
        mobile_page.open(route_type=route_type)
        mobile_page.mobile_map.click_project("arisha")

    with allure.step("Кликаем на Explore Project"):
        mobile_page.mobile_map.click_explore_project("arisha")

    with allure.step("Кликаем на All units"):
        mobile_page.navigate_to_mobile_arisha_all_units()

    with allure.step("Ищем и кликаем на первый доступный апартамент"):
        mobile_page.mobile_navigation.find_and_click_available_apartment()

    mobile_page.wait_for_apartment_widget_load()

    with allure.step("Кликаем на кнопку 2D"):
        mobile_page.apartment_widget.switch_to_2d_mode()
        mobile_page.page.wait_for_timeout(1000)

    with allure.step("Проверяем появление навигации в режиме 2D"):
        arrows_visible = mobile_page.apartment_widget.check_navigation_arrows_visible()
        mobile_page.assertions.assert_that(
            arrows_visible, "Стрелочки навигации не появились в режиме 2D"
        )
        mobile_page.page.wait_for_timeout(1000)

    with allure.step("Кликаем на стрелочки для просмотра слайдов"):
        initial_scene = mobile_page.apartment_widget.get_current_scene()
        if initial_scene:
            allure.attach(
                f"Начальная сцена: {initial_scene}",
                name="Initial Scene",
                attachment_type=allure.attachment_type.TEXT,
            )

        # Просматриваем несколько слайдов
        scenes = mobile_page.apartment_widget.navigate_to_next_slide(3)

        for i, scene in enumerate(scenes):
            if scene:
                allure.attach(
                    f"Слайд #{i+1}: {scene}",
                    name=f"Slide {i+1}",
                    attachment_type=allure.attachment_type.TEXT,
                )

        mobile_page.page.wait_for_timeout(1000)

    with allure.step("Кликаем на кнопку 3D"):
        mobile_page.apartment_widget.switch_to_3d_mode()
        mobile_page.page.wait_for_timeout(1000)

        # Проверяем, что кнопка 3D стала активной
        button_active = mobile_page.apartment_widget.check_mode_button_active("3D")
        mobile_page.assertions.assert_that(button_active, "Кнопка 3D не стала активной")

    with allure.step("Делаем скриншот финального состояния"):
        screenshot = mobile_page.apartment_widget.take_widget_screenshot()
        allure.attach(
            screenshot,
            name="Final Widget State",
            attachment_type=allure.attachment_type.PNG,
        )

    with allure.step("Проверяем адаптивность на мобильном устройстве"):
        mobile_page.check_mobile_viewport_adaptation()
