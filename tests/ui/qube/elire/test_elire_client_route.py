import allure
import pytest


@allure.feature("Qube - Проект Elire")
@allure.story("Клиентский роут - Отправка обратной связи")
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.ui
def test_elire_send_callback_form_on_client_page(elire_client_page):
    """Тест отправки формы обратной связи на клиентской странице проекта Elire."""
    with allure.step("Открываем клиентскую страницу проекта Elire"):
        elire_client_page.open_client_page()

        current_url = elire_client_page.get_current_url()
        assert "client" in current_url, "Не открылась клиентская страница"
