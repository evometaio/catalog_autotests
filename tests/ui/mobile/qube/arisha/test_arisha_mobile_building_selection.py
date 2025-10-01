import allure
import pytest


@allure.feature("Qube - Проект Arisha (Mobile)")
@allure.story("Мобильная навигация по зданиям")
@pytest.mark.mobile
@pytest.mark.ui
@pytest.mark.smoke
class TestArishaMobileBuildingSelection:
    """Мобильные тесты навигации по зданиям Arisha."""

    @allure.severity(allure.severity_level.CRITICAL)
    def test_arisha_mobile_building_selection(self, mobile_map_page):
        """Тест мобильной навигации по зданиям проекта Arisha."""

        with allure.step("1. Открываем мобильную карту и переходим к проекту Arisha"):
            mobile_map_page.open(route_type="map")

            # Кликаем по проекту Arisha
            mobile_map_page.click(locators.get("MAP_LOCATOR"))

            # Кликаем на кнопку "Explore Project"
            mobile_map_page.click(
                '[data-test-id="map-project-point-button-mobile-arisha"]'
            )

            # Даем время на загрузку страницы
            import time

            time.sleep(3)

        with allure.step("2. Проверяем наличие кнопки 'Choose the building'"):
            choose_building_button = mobile_map_page.page.locator(
                'button:has-text("Choose the building")'
            )
            assert (
                choose_building_button.is_visible()
            ), "Кнопка 'Choose the building' не найдена"

            # Кликаем на кнопку (используем force=True для обхода перекрытия)
            choose_building_button.click(force=True)
            allure.attach(
                "Кнопка 'Choose the building' найдена и нажата",
                name="Building Selection",
            )

        with allure.step("3. Проверяем SVG элементы зданий"):
            building_elements = mobile_map_page.page.locator(
                'svg path[class*="_building_"]'
            )
            building_count = building_elements.count()
            assert building_count > 0, "SVG элементы зданий не найдены"

            allure.attach(
                f"Найдено SVG элементов зданий: {building_count}",
                name="Building SVG Count",
            )

            # Проверяем активное здание
            active_building = mobile_map_page.page.locator(
                'svg path[class*="_animationActive_"]'
            )
            active_count = active_building.count()
            if active_count > 0:
                allure.attach(
                    f"Найдено активных зданий: {active_count}",
                    name="Active Building Count",
                )

        with allure.step("4. Проверяем мобильную навигацию"):
            compact_nav = mobile_map_page.page.locator(
                ".CompactNavigation_navigationContainer__Y5mfa._showOnMobiles_1xz7w_17"
            )
            assert compact_nav.is_visible(), "Мобильная компактная навигация не найдена"

            nav_text = compact_nav.text_content()
            allure.attach(
                f"Текст мобильной навигации: {nav_text[:100]}",
                name="Mobile Navigation Text",
            )

        with allure.step("5. Проверяем доступные кнопки управления"):
            # Кнопка 360° просмотра (используем .first для обхода дублирования)
            rotation_button = mobile_map_page.page.locator(
                '[data-test-id="nav-rotation-view-controls-button"]'
            ).first
            if rotation_button.is_visible():
                allure.attach("Кнопка 360° просмотра найдена", name="360° Button")

            # Кнопка "Get brochure"
            brochure_button = mobile_map_page.page.locator(
                '[data-test-id="contact-button"]'
            )
            if brochure_button.is_visible():
                allure.attach("Кнопка 'Get brochure' найдена", name="Brochure Button")

            # Кнопка назад
            back_button = mobile_map_page.page.locator(
                '[data-test-id="nav-button-back"]'
            )
            if back_button.is_visible():
                allure.attach("Кнопка 'Назад' найдена", name="Back Button")

        with allure.step("6. Финальная проверка"):
            # Проверяем, что основные элементы все еще видны
            compact_nav = mobile_map_page.page.locator(
                ".CompactNavigation_navigationContainer__Y5mfa._showOnMobiles_1xz7w_17"
            )
            assert compact_nav.is_visible(), "Мобильная навигация исчезла"

            allure.attach("Все проверки пройдены успешно", name="Final Check")
