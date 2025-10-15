import allure
import pytest


@allure.feature("Qube - Проект Arisha (mobile)")
@allure.story("Клиентский роут - Отправка обратной связи - Мобильная")
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.mobile
@pytest.mark.skip(reason="Реализовать на DEV")
def test_arisha_mobile_send_callback_form_on_client_page(mobile_page):
    """Тест отправки формы обратной связи на клиентской странице проекта Arisha на мобильном устройстве."""
    pass
