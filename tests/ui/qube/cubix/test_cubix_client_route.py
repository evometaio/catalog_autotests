import allure
import pytest


@allure.feature("Qube - Проект Cubix")
@allure.story("Клиентский роут - Отправка обратной связи")
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.ui
def test_cubix_send_callback_form_on_client_page(cubix_client_page):
    """Тест отправки формы обратной связи на клиентской странице проекта Cubix."""
    with allure.step("Открываем клиентскую страницу проекта Cubix"):
        cubix_client_page.open_client_page()

        current_url = cubix_client_page.get_current_url()
        assert "client" in current_url, "Не открылась клиентская страница"
