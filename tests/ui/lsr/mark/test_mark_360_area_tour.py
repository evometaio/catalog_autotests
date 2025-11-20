import os

import allure
import pytest


@allure.feature("LSR - Проект MARK")
@allure.story("360 тур по территории")
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.ui
@pytest.mark.skipif(
    os.getenv("TEST_ENVIRONMENT", "prod") != "dev",
    reason="Тест запускается только на dev окружении",
)
@pytest.mark.parametrize(
    "panorama_type", ["rotation", "yard", "lobby-k1", "lobby-k2", "lobby-k3"]
)
def test_mark_360_area_tour(mark_page, panorama_type):
    """Тест 360 Area Tour для проекта MARK с разными типами панорам."""
    with allure.step("Открываем главную страницу MARK"):
        mark_page.open()

    with allure.step("Кликаем на кнопку 360 Area Tour (Панорамы)"):
        mark_page.area_tour_360.click_360_button()

    with allure.step(f"Кликаем на пункт меню: {panorama_type}"):
        mark_page.area_tour_360.click_360_menu_item(panorama_type)

    # Для rotation типа проверяем модальное окно, для остальных - iframe контент
    if panorama_type == "rotation":
        with allure.step("Проверяем отображение модального окна 360 Area Tour"):
            mark_page.area_tour_360.verify_modal_displayed()

        with allure.step("Проверяем наличие контента в модальном окне"):
            mark_page.area_tour_360.verify_content()

        with allure.step("Закрываем модальное окно 360 Area Tour"):
            mark_page.area_tour_360.close_modal()
    else:
        with allure.step(
            "Проверяем, что URL изменился (добавился hash с типом панорамы)"
        ):
            current_url = mark_page.get_current_url()
            assert (
                f"#tour3d={panorama_type}" in current_url
                or f"tour3d={panorama_type}" in current_url
            ), f"URL не содержит информацию о выбранной панораме. Текущий URL: {current_url}"

        with allure.step("Проверяем наличие контента 360 тура (iframe)"):
            iframe = mark_page.page.locator("iframe")
            iframe.first.wait_for(state="attached", timeout=10000)
            assert iframe.count() > 0, "Контент 360 тура (iframe) не найден на странице"
