import allure
import pytest


@allure.feature("Wellcube - Проект Tranquil")
@allure.story("Карта")
@pytest.mark.smoke
@pytest.mark.ui
def test_tranquil_map_page(wellcube_map_page):
    """Тест карты проекта Wellcube (Tranquil)."""
    # TODO: Реализовать тест после создания фикстур для Wellcube
    with allure.step("Открываем карту Wellcube (Tranquil)"):
        # wellcube_map_page.open_map_page()
        pass

    with allure.step("Проверяем функциональность карты"):
        # TODO: Добавить проверки для Wellcube (Tranquil)
        pass
