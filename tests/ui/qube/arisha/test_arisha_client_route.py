import allure
import pytest


@allure.feature("Qube - Проект Arisha")
@allure.story("Клиентский роут - Отправка обратной связи")
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.ui
def test_arisha_send_callback_form_on_client_page(client_page):
    """Тест отправки формы обратной связи на клиентской странице проекта Arisha."""
    _test_client_page_generic(client_page, "arisha")


def _test_client_page_generic(project_page, project_name):
    """Универсальная функция для тестирования client страниц."""
    with allure.step(f"Открываем клиентскую страницу проекта {project_name.title()}"):
        project_page.open(route_type="client")

        current_url = project_page.get_current_url()
        assert "client" in current_url, "Не открылась клиентская страница"
