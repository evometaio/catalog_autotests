import allure
import pytest


@allure.feature("Qube - Проект Elire (mobile)")
@allure.story("Агентский роут - Мобильная")
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.mobile
@pytest.mark.skip(reason="Desktop тест не реализован")
def test_elire_mobile_agent_route(mobile_page):
    """Тест агентского роута для проекта Elire на мобильном устройстве."""
    pass
