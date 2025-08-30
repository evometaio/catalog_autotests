import allure
import pytest

@allure.feature("Страница проекта (клиентский роут)")
@allure.story("Отправка обратной связи")
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.ui
@allure.severity(allure.severity_level.CRITICAL)
def test_send_callback_form_on_project_client_page(project_client_page):
    with allure.step("Открываем клиенсткую страницу"):
        project_client_page.open_client_page()

        current_url = project_client_page.get_current_url()
        assert "client" in current_url, "Не открылась клиентская страница"

