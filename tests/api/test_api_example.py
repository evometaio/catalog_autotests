import allure
import pytest
import requests


@allure.feature("API")
@allure.story("Базовые запросы (Шаблон теста API)")
@pytest.mark.skip(reason="Пример теста")
@allure.severity(allure.severity_level.MINOR)
def test_api_health_check():
    """Тест проверки здоровья API."""
    with allure.step("Отправляем GET запрос"):
        response = requests.get("https://httpbin.org/status/200", timeout=10)

    with allure.step("Проверяем статус ответа"):
        assert (
            response.status_code == 200
        ), f"Ожидался статус 200, получен: {response.status_code}"
