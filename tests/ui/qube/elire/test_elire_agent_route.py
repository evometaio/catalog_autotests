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
    pass
