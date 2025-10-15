import allure
import pytest


@allure.feature("Qube - Проект Arisha")
@allure.story("Клиентский роут - Отправка обратной связи")
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.ui
@pytest.mark.skip(reason="Реализовать на DEV")
def test_arisha_send_callback_form_on_client_page(arisha_page):
    """Тест отправки формы обратной связи на клиентской странице проекта Arisha."""
    pass
