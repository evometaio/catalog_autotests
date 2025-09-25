import os

import allure
import pytest


@allure.feature("Qube - Проект Arisha")
@allure.story("Виджет апартамента - Полный функционал")
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.ui
@pytest.mark.skipif(
    os.getenv("OS_PLATFORM") == "ubuntu-latest",
    reason="Тест нестабилен на Firefox в CI",
)
def test_arisha_apartment_widget_full_functionality(map_page):
    """Тест полного функционала виджета апартамента Arisha."""

    with allure.step("Открываем страницу апартамента Arisha"):
        map_page.apartment_widget.open_apartment_page("arisha", "104")

        # Проверяем наличие кнопок режимов
        frame_locator = map_page.apartment_widget.get_widget_frame()

        # Получаем локаторы для проверки видимости кнопок
        widget_locators = map_page.project_locators.Arisha.ApartmentWidget()
        view_2d_button = frame_locator.locator(widget_locators.VIEW_2D_BUTTON)
        view_3d_button = frame_locator.locator(widget_locators.VIEW_3D_BUTTON)

        view_2d_button.wait_for(state="visible", timeout=15000)
        view_3d_button.wait_for(state="visible", timeout=15000)

        allure.attach(
            "Кнопки режимов 2D/3D найдены",
            name="Initial State",
            attachment_type=allure.attachment_type.TEXT,
        )

    with allure.step("Кликаем на кнопку 2D"):
        map_page.apartment_widget.switch_to_2d_mode("arisha")

        # Ждем появления навигационных стрелок в режиме 2D
        map_page.apartment_widget.get_widget_frame().locator(
            map_page.project_locators.Arisha.ApartmentWidget().NEXT_ARROW
        ).first.wait_for(state="visible", timeout=2000)

        allure.attach(
            "Переключились в режим 2D",
            name="2D Mode",
            attachment_type=allure.attachment_type.TEXT,
        )

    with allure.step("Проверяем появление навигации в режиме 2D"):
        assert map_page.apartment_widget.check_navigation_arrows_visible(
            "arisha"
        ), "Стрелочки навигации не появились в режиме 2D"
        allure.attach(
            "Навигация по сценам доступна в режиме 2D",
            name="2D Navigation",
            attachment_type=allure.attachment_type.TEXT,
        )

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

        # Ждем стабилизации после навигации по слайдам
        map_page.apartment_widget.get_widget_frame().locator(
            map_page.project_locators.Arisha.ApartmentWidget().SCENE_INDICATOR
        ).first.wait_for(state="visible", timeout=2000)

        allure.attach(
            "Просмотрели несколько слайдов",
            name="Slides Navigation",
            attachment_type=allure.attachment_type.TEXT,
        )

    with allure.step("Кликаем на кнопку 3D"):
        map_page.apartment_widget.switch_to_3d_mode("arisha")

        # Ждем стабилизации интерфейса - ждем появления кнопки 3D
        view_3d_button = map_page.apartment_widget.get_widget_frame().locator(
            map_page.project_locators.Arisha.ApartmentWidget().VIEW_3D_BUTTON
        )
        view_3d_button.wait_for(state="visible", timeout=2000)

        # Проверяем, что кнопка 3D стала активной
        assert map_page.apartment_widget.check_mode_button_active(
            "arisha", "3D"
        ), "Кнопка 3D не стала активной"
        allure.attach(
            "Переключились в режим 3D",
            name="3D Mode",
            attachment_type=allure.attachment_type.TEXT,
        )

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
def test_arisha_apartment_information(map_page):
    """Тест проверки информации об апартаменте Arisha."""

    with allure.step("Открываем страницу апартамента Arisha"):
        map_page.apartment_widget.open_apartment_page("arisha", "104")

        # Ждем появления информации об апартаменте
        map_page.apartment_info.wait_for_info_to_appear("arisha")
        allure.attach(
            "Информация об апартаменте появилась",
            name="Info Appeared",
            attachment_type=allure.attachment_type.TEXT,
        )

    with allure.step("Проверяем номер апартамента"):
        apartment_number_correct = map_page.apartment_info.check_apartment_number(
            "arisha", "104"
        )
        assert apartment_number_correct, "Номер апартамента APT. 104 не найден"
        allure.attach(
            "Номер апартамента APT. 104 корректный",
            name="Apartment Number",
            attachment_type=allure.attachment_type.TEXT,
        )

    with allure.step("Проверяем тип апартамента"):
        type_visible = map_page.apartment_info.check_apartment_type("arisha")
        assert type_visible, "Тип апартамента '2 Bedroom' не найден"
        allure.attach(
            "Тип апартамента '2 Bedroom' отображается",
            name="Apartment Type",
            attachment_type=allure.attachment_type.TEXT,
        )

    with allure.step("Проверяем информацию о этаже (опционально)"):
        floor_visible = map_page.apartment_info.check_floor_info("arisha")
        if floor_visible:
            allure.attach(
                "Этаж 'Floor: 1' отображается",
                name="Floor Info",
                attachment_type=allure.attachment_type.TEXT,
            )
        else:
            allure.attach(
                "Информация о этаже не найдена (может отсутствовать на продакшене)",
                name="Floor Info",
                attachment_type=allure.attachment_type.TEXT,
            )

    with allure.step("Проверяем информацию о здании"):
        building_visible = map_page.apartment_info.check_building_info("arisha")
        assert building_visible, "Информация о здании 'Building: 1' не найдена"
        allure.attach(
            "Здание 'Building: 1' отображается",
            name="Building Info",
            attachment_type=allure.attachment_type.TEXT,
        )

    with allure.step("Проверяем информацию о площади"):
        area_visible = map_page.apartment_info.check_area_info("arisha")
        assert area_visible, "Информация о площади '1 090,38 sq ft' не найдена"
        allure.attach(
            "Площадь '1 090,38 sq ft' отображается",
            name="Area Info",
            attachment_type=allure.attachment_type.TEXT,
        )

    with allure.step("Проверяем информацию о виде"):
        view_visible = map_page.apartment_info.check_view_info("arisha")
        assert view_visible, "Информация о виде 'Green Community' не найдена"
        allure.attach(
            "Вид 'Green Community' отображается",
            name="View Info",
            attachment_type=allure.attachment_type.TEXT,
        )

    with allure.step("Проверяем особенности апартамента"):
        features = map_page.apartment_info.check_features("arisha")

        assert features[
            "modern_design"
        ], "Особенность 'Modern interior design' не найдена"
        assert features[
            "high_quality"
        ], "Особенность 'High quality materials' не найдена"
        assert features[
            "built_in_appliances"
        ], "Особенность 'Built-in appliances' не найдена"

        allure.attach(
            "Все особенности апартамента отображаются",
            name="Features",
            attachment_type=allure.attachment_type.TEXT,
        )

    with allure.step("Проверяем счетчик просмотров"):
        watching_visible = map_page.apartment_info.check_watching_count("arisha")
        assert watching_visible, "Счетчик просмотров 'watching now' не найден"
        allure.attach(
            "Счетчик просмотров 'watching now' отображается",
            name="Watching Count",
            attachment_type=allure.attachment_type.TEXT,
        )

    with allure.step("Получаем полный текст информации для проверки"):
        info_text = map_page.apartment_info.get_info_text("arisha")
        allure.attach(
            info_text,
            name="Full Info Text",
            attachment_type=allure.attachment_type.TEXT,
        )

        # Проверяем наличие всех ключевых элементов в тексте
        expected_elements = [
            "APT. 104",
            "2 Bedroom",
            "Building:",
            "Total area:",
            "Green Community",
            "Modern interior design",
            "High quality materials",
            "Built-in appliances",
            "watching now",
        ]

        for element in expected_elements:
            assert (
                element in info_text
            ), f"Элемент '{element}' не найден в тексте информации"

        allure.attach(
            "Все ключевые элементы найдены в тексте информации",
            name="Text Verification",
            attachment_type=allure.attachment_type.TEXT,
        )

    with allure.step("Делаем скриншот информации об апартаменте"):
        info_screenshot = map_page.apartment_info.take_info_screenshot("arisha")
        allure.attach(
            info_screenshot,
            name="Apartment Info Screenshot",
            attachment_type=allure.attachment_type.PNG,
        )
