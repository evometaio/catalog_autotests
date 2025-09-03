import allure
import pytest


@allure.feature("Qube - Проект Elire")
@allure.story("Агентский роут - Загрузка PDF")
@pytest.mark.smoke
@pytest.mark.skip(reason="Нет такого функционала")
@pytest.mark.regression
@pytest.mark.ui
def test_elire_download_pdf_on_agent_page(agent_page):
    """Тест скачивания PDF на агентской странице проекта Elire."""
    with allure.step("Выполняем полный цикл тестирования PDF для проекта Elire"):
        success, file_path = agent_page.test_pdf_download_workflow("elire")
        assert success, f"PDF тест не прошел успешно: {file_path}"
