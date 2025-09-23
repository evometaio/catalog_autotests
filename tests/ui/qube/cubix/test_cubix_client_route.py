import allure
import pytest


@allure.feature("Qube - Проект Cubix")
@allure.story("Клиентский роут - Отправка обратной связи")
@pytest.mark.skip(reason="Не работает")
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.ui
def test_cubix_send_callback_form_on_client_page(client_page):
    """Тест отправки формы обратной связи на клиентской странице проекта Cubix."""
    pass


@allure.feature("Qube - Проект Cubix")
@allure.story("Клиентский роут - Форма Register Interest")
@pytest.mark.skip(reason="Нужно реализовать")
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.ui
def test_cubix_request_viewing_form_with_mock(client_page, fake):
    """Тест формы Register Interest проекта Cubix."""

    with allure.step("Открываем клиентскую страницу проекта Cubix"):
        client_page.open(route_type="client")

    ## написать код
