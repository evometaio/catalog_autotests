import allure
import pytest


@allure.feature("Qube - Проект Cubix (mobile)")
@allure.story("Клиентский роут - Мобильная")
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.mobile
@pytest.mark.skip(reason="Desktop тест не реализован")
def test_cubix_mobile_client_route(mobile_page):
    """Тест клиентского роута для проекта Cubix на мобильном устройстве."""
    pass
