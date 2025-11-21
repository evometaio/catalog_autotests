import os
import time

import allure
import pytest


@allure.feature("LSR - Проект MARK (mobile)")
@allure.story("360 тур по территории")
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.mobile
@pytest.mark.skipif(
    os.getenv("TEST_ENVIRONMENT", "prod") != "dev",
    reason="Тест запускается только на dev окружении",
)
@pytest.mark.parametrize(
    "panorama_type",
    ["rotation", "yard", "lobby-k1", "lobby-k2", "lobby-k3"],
)
def test_mark_mobile_360_area_tour(mark_page, panorama_type):
    """Тест 360 Area Tour для MARK на мобильном устройстве с разными типами панорам."""
    with allure.step("Открываем главную страницу MARK (mobile)"):
        mark_page.open()

    with allure.step("Кликаем на кнопку 360 Area Tour (Панорамы, mobile)"):
        # Используем общий компонент, который уже учитывает особенности MARK на мобилке
        mark_page.area_tour_360.click_360_button()

    if panorama_type == "rotation":
        with allure.step("Проверяем 360-панораму rotation (модальное окно)"):
            mark_page.area_tour_360.verify_modal_displayed()
            mark_page.area_tour_360.verify_content()
            mark_page.area_tour_360.close_modal()
        return

    with allure.step(f"Кликаем на пункт меню панорам: {panorama_type}"):
        mark_page.area_tour_360.click_360_menu_item(panorama_type)

    with allure.step("Проверяем, что URL содержит выбранную панораму"):
        current_url = mark_page.get_current_url()
        assert (
            f"#tour3d={panorama_type}" in current_url
            or f"tour3d={panorama_type}" in current_url
        ), f"URL не содержит выбранную панораму ({panorama_type}). Текущий URL: {current_url}"

    with allure.step("Проверяем наличие контента 360 тура (iframe/canvas/video)"):
        iframe = mark_page.page.locator("iframe")
        canvas = mark_page.page.locator("canvas")
        video = mark_page.page.locator("video")

        if iframe.count() > 0:
            iframe.first.wait_for(state="attached", timeout=10000)
        elif canvas.count() > 0:
            canvas.first.wait_for(state="attached", timeout=10000)
        elif video.count() > 0:
            video.first.wait_for(state="attached", timeout=10000)

        total_content = iframe.count() + canvas.count() + video.count()
        assert total_content > 0, "Контент 360 тура не найден на мобильной странице"
