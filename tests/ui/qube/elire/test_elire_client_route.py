import os

import allure
import pytest

from tests.ui.qube.arisha.test_arisha_client_route import _test_client_page_generic


@allure.feature("Qube - Проект Elire")
@allure.story("Клиентский роут - Отправка обратной связи")
@pytest.mark.skip(reason="Не работает")
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.ui
def test_elire_send_callback_form_on_client_page(client_page):
    """Тест отправки формы обратной связи на клиентской странице проекта Elire."""
    _test_client_page_generic(client_page, "elire")


@allure.feature("Qube - Проект Elire")
@allure.story("Клиентский роут - Форма Request Viewing")
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.ui
def test_elire_request_viewing_form(client_page, fake):
    """Тест формы Request Viewing"""

    # Проверяем, что тест запускается только на DEV окружении
    env = os.getenv("TEST_ENVIRONMENT", "prod")
    if env != "dev":
        pytest.skip(
            f"Тест запускается только на DEV окружении. Текущее окружение: {env}"
        )

    with allure.step("Открываем клиентскую страницу проекта Elire"):
        client_page.open(route_type="client")

        current_url = client_page.get_current_url()
        assert "client" in current_url, "Не открылась клиентская страница"

    with allure.step("Кликаем на проект Elire"):
        client_page.click_project_on_map("elire")

    with allure.step("Кликаем на Request Viewing"):
        client_page.click_on_residences_button_and_request_viewing_form()

    with allure.step("Заполняем и отправляем форму Request Viewing"):
        # Заполняем и отправляем форму
        client_page.fill_and_submit_request_viewing_form(fake)

    with allure.step("Проверяем успешную отправку формы"):
        client_page.page.wait_for_timeout(3000)

        success_displayed = client_page.is_success_message_displayed()
        assert success_displayed, "Сообщение об успешной отправке не отображается"
