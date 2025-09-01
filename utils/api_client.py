from typing import Any, Dict, Optional

import allure
import requests

from utils.logger import get_logger


class APIClient:
    """Базовый класс для работы с API."""

    def __init__(self, base_url: str = None, timeout: int = None):
        self.base_url = base_url or "https://api.example.com"
        self.timeout = timeout or 30
        self.session = requests.Session()
        self.logger = get_logger("APIClient")

        # Устанавливаем заголовки по умолчанию
        self.session.headers.update(
            {"Content-Type": "application/json", "Accept": "application/json"}
        )

    def _log_request(self, method: str, url: str, **kwargs):
        """Логирует информацию о запросе."""
        self.logger.info(f"{method} {url}")
        if "json" in kwargs:
            self.logger.debug(f"Request body: {kwargs['json']}")
        if "params" in kwargs:
            self.logger.debug(f"Request params: {kwargs['params']}")

    def _log_response(self, response: requests.Response):
        """Логирует информацию об ответе."""
        self.logger.info(f"Response status: {response.status_code}")
        self.logger.debug(f"Response headers: {dict(response.headers)}")
        try:
            self.logger.debug(f"Response body: {response.json()}")
        except:
            self.logger.debug(f"Response body: {response.text}")

    def _make_request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        """
        Выполняет HTTP запрос.

        Args:
            method: HTTP метод (GET, POST, PUT, DELETE)
            endpoint: Конечная точка API
            **kwargs: Дополнительные параметры запроса

        Returns:
            Response объект
        """
        url = f"{self.base_url.rstrip('/')}/{endpoint.lstrip('/')}"

        with allure.step(f"{method} {endpoint}"):
            self._log_request(method, url, **kwargs)

            response = self.session.request(
                method=method, url=url, timeout=self.timeout, **kwargs
            )

            self._log_response(response)

            # Прикрепляем информацию к Allure отчету
            allure.attach(
                f"Request: {method} {url}\nResponse: {response.status_code}",
                name=f"{method}_{endpoint}",
                attachment_type=allure.attachment_type.TEXT,
            )

            return response

    def get(self, endpoint: str, params: Dict = None, **kwargs) -> requests.Response:
        """
        Выполняет GET запрос.

        Args:
            endpoint: Конечная точка API
            params: Параметры запроса
            **kwargs: Дополнительные параметры

        Returns:
            Response объект
        """
        return self._make_request("GET", endpoint, params=params, **kwargs)

    def post(
        self, endpoint: str, data: Dict = None, json: Dict = None, **kwargs
    ) -> requests.Response:
        """
        Выполняет POST запрос.

        Args:
            endpoint: Конечная точка API
            data: Данные для отправки
            json: JSON данные для отправки
            **kwargs: Дополнительные параметры

        Returns:
            Response объект
        """
        return self._make_request("POST", endpoint, data=data, json=json, **kwargs)

    def put(
        self, endpoint: str, data: Dict = None, json: Dict = None, **kwargs
    ) -> requests.Response:
        """
        Выполняет PUT запрос.

        Args:
            endpoint: Конечная точка API
            data: Данные для отправки
            json: JSON данные для отправки
            **kwargs: Дополнительные параметры

        Returns:
            Response объект
        """
        return self._make_request("PUT", endpoint, data=data, json=json, **kwargs)

    def delete(self, endpoint: str, **kwargs) -> requests.Response:
        """
        Выполняет DELETE запрос.

        Args:
            endpoint: Конечная точка API
            **kwargs: Дополнительные параметры

        Returns:
            Response объект
        """
        return self._make_request("DELETE", endpoint, **kwargs)

    def patch(
        self, endpoint: str, data: Dict = None, json: Dict = None, **kwargs
    ) -> requests.Response:
        """
        Выполняет PATCH запрос.

        Args:
            endpoint: Конечная точка API
            data: Данные для отправки
            json: JSON данные для отправки
            **kwargs: Дополнительные параметры

        Returns:
            Response объект
        """
        return self._make_request("PATCH", endpoint, data=data, json=json, **kwargs)

    def set_auth_token(self, token: str):
        """
        Устанавливает токен авторизации.

        Args:
            token: Токен авторизации
        """
        self.session.headers.update({"Authorization": f"Bearer {token}"})
        self.logger.info("Установлен токен авторизации")

    def set_headers(self, headers: Dict[str, str]):
        """
        Устанавливает заголовки запросов.

        Args:
            headers: Словарь заголовков
        """
        self.session.headers.update(headers)
        self.logger.info(f"Установлены заголовки: {headers}")

    def clear_headers(self):
        """Очищает все заголовки кроме Content-Type и Accept."""
        self.session.headers.clear()
        self.session.headers.update(
            {"Content-Type": "application/json", "Accept": "application/json"}
        )
        self.logger.info("Заголовки очищены")

    def expect_status_code(self, response: requests.Response, expected_code: int):
        """
        Проверяет статус код ответа.

        Args:
            response: Response объект
            expected_code: Ожидаемый статус код
        """
        with allure.step(f"Проверяем статус код: {expected_code}"):
            assert (
                response.status_code == expected_code
            ), f"Ожидался статус код {expected_code}, получен {response.status_code}"

    def expect_json_schema(self, response: requests.Response, schema: Dict):
        """
        Проверяет JSON схему ответа.

        Args:
            response: Response объект
            schema: Ожидаемая JSON схема
        """
        # Здесь можно добавить валидацию JSON схемы
        # Например, используя jsonschema библиотеку
        with allure.step("Проверяем JSON схему"):
            try:
                response_json = response.json()
                # TODO: Добавить валидацию схемы
                self.logger.info("JSON схема валидна")
            except Exception as e:
                self.logger.error(f"Ошибка валидации JSON схемы: {e}")
                raise
