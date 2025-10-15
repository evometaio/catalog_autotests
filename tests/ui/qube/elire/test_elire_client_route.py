import os

import allure
import pytest


@allure.feature("Qube - Проект Elire")
@allure.story("Клиентский роут - Форма Request Viewing")
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.ui
def test_elire_request_viewing_form(elire_page, fake):
    """Тест формы Request Viewing"""

    # Проверяем, что тест запускается только на DEV окружении
    env = os.getenv("TEST_ENVIRONMENT", "prod")
    if env != "dev":
        pytest.skip(
            f"Тест запускается только на DEV окружении. Текущее окружение: {env}"
        )

    with allure.step("Открываем клиентскую страницу проекта Elire"):
        elire_page.open(route_type="client")
        elire_page.assertions.assert_url_contains(
            "client", "Не открылась клиентская страница"
        )

    with allure.step("Кликаем на проект Elire"):
        elire_page.map.navigate_to_project("elire")

    with allure.step("Кликаем на Request Viewing"):
        elire_page.click_residences_button_and_request_viewing_form()

    with allure.step("Заполняем и отправляем форму Request Viewing"):
        elire_page.fill_and_submit_request_viewing_form(fake)

    with allure.step("Проверяем успешную отправку формы"):
        # Ждем появления модального окна с сообщением об успехе
        elire_page.page.wait_for_selector(
            elire_page.project_locators.SUCCESS_MODAL,
            state="visible",
            timeout=5000,
        )

        success_displayed = elire_page.is_success_message_displayed()
        elire_page.assertions.assert_that(
            success_displayed,
            "Модальное окно с сообщением об успешной отправке не отображается",
        )
