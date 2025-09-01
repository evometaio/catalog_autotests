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


# TODO шаблоны для будущих API тестов
# @allure.feature("API")
# @allure.story("POST запросы")
# @pytest.mark.skip(reason="Пример теста")
# @pytest.mark.smoke
# @pytest.mark.api
# @allure.severity(allure.severity_level.CRITICAL)
# def test_api_post_request():
#     """Тест POST запроса."""
#     test_data = {"name": "test", "value": 123}
#
#     with allure.step("Отправляем POST запрос с данными"):
#         response = requests.post(
#             "https://httpbin.org/post",
#             json=test_data,
#             timeout=10
#         )
#
#     with allure.step("Проверяем ответ"):
#         assert response.status_code == 200, f"Ожидался статус 200, получен: {response.status_code}"
#
#         response_data = response.json()
#         assert response_data["json"]["name"] == "test", "Имя не соответствует ожидаемому"
#         assert response_data["json"]["value"] == 123, "Значение не соответствует ожидаемому"
#
#
# @allure.feature("API")
# @allure.story("Обработка ошибок")
# @pytest.mark.skip(reason="Пример теста")
# @pytest.mark.regression
# @pytest.mark.api
# @allure.severity(allure.severity_level.NORMAL)
# def test_api_error_handling():
#     """Тест обработки ошибок API."""
#     with allure.step("Отправляем запрос к несуществующему эндпоинту"):
#         try:
#             response = requests.get("https://httpbin.org/status/404", timeout=10)
#             assert response.status_code == 404, f"Ожидался статус 404, получен: {response.status_code}"
#         except requests.exceptions.RequestException as e:
#             allure.attach(
#                 str(e),
#                 name="error_details",
#                 attachment_type=allure.attachment_type.TEXT
#             )
#             raise
#
#
# @allure.feature("API")
# @allure.story("Валидация данных")
# @pytest.mark.skip(reason="Пример теста")
# @pytest.mark.regression
# @pytest.mark.api
# @allure.severity(allure.severity_level.NORMAL)
# def test_api_data_validation():
#     """Тест валидации данных API."""
#     test_data = {
#         "string": "test_string",
#         "number": 42,
#         "boolean": True,
#         "array": [1, 2, 3],
#         "object": {"key": "value"}
#     }
#
#     with allure.step("Отправляем POST запрос с различными типами данных"):
#         response = requests.post(
#             "https://httpbin.org/post",
#             json=test_data,
#             timeout=10
#         )
#
#     with allure.step("Проверяем статус ответа"):
#         assert response.status_code == 200, f"Ожидался статус 200, получен: {response.status_code}"
#
#     with allure.step("Проверяем валидацию полученных данных"):
#         response_data = response.json()
#         received_data = response_data["json"]
#
#         # Проверяем, что все данные получены корректно
#         assert received_data["string"] == "test_string", "Строка не соответствует ожидаемой"
#         assert received_data["number"] == 42, "Число не соответствует ожидаемому"
#         assert received_data["boolean"] == True, "Булево значение не соответствует ожидаемому"
#         assert received_data["array"] == [1, 2, 3], "Массив не соответствует ожидаемому"
#         assert received_data["object"] == {"key": "value"}, "Объект не соответствует ожидаемому"
#
#
# @allure.feature("API")
# @allure.story("Производительность")
# @pytest.mark.skip(reason="Пример теста")
# @pytest.mark.regression
# @pytest.mark.api
# @allure.severity(allure.severity_level.MINOR)
# def test_api_performance():
#     """Тест производительности API."""
#     import time
#
#     with allure.step("Измеряем время ответа API"):
#         start_time = time.time()
#         response = requests.get("https://httpbin.org/delay/1", timeout=15)
#         end_time = time.time()
#
#         response_time = end_time - start_time
#
#     with allure.step("Проверяем статус ответа"):
#         assert response.status_code == 200, f"Ожидался статус 200, получен: {response.status_code}"
#
#     with allure.step("Проверяем время ответа"):
#         # API должен ответить в разумное время (не более 5 секунд)
#         assert response_time < 5.0, f"Время ответа слишком велико: {response_time:.2f}с"
#
#         # Прикрепляем время ответа к отчету
#         allure.attach(
#             f"Время ответа API: {response_time:.2f} секунд",
#             name="response_time",
#             attachment_type=allure.attachment_type.TEXT
#         )
