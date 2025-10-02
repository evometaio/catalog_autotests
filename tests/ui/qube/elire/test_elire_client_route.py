import os

import allure
import pytest


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
        client_page.project.click_on_residences_button_and_request_viewing_form()

    with allure.step("Заполняем и отправляем форму Request Viewing"):
        # Заполняем и отправляем форму
        client_page.project.fill_and_submit_request_viewing_form(fake)

    with allure.step("Проверяем успешную отправку формы"):
        # Ждем появления модального окна с сообщением об успехе
        client_page.page.wait_for_selector(
            client_page.project_locators.Elire.SUCCESS_MODAL,
            state="visible",
            timeout=5000,
        )

        success_displayed = client_page.project.is_success_message_displayed()
        assert success_displayed, "Сообщение об успешной отправке не отображается"
