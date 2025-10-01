"""
Кастомные исключения для автотестов.

Этот модуль содержит все исключения, используемые в фреймворке автотестов.
"""


class AutotestException(Exception):
    """Базовое исключение для автотестов."""

    def __init__(self, message: str, details: str = None):
        super().__init__(message)
        self.message = message
        self.details = details or ""


class ConfigurationError(AutotestException):
    """Ошибка конфигурации."""

    pass


class ElementNotFoundError(AutotestException):
    """Элемент не найден на странице."""

    def __init__(self, selector: str, timeout: int = None, details: str = None):
        timeout_msg = f" за {timeout}ms" if timeout else ""
        message = f"Элемент '{selector}' не найден{timeout_msg}"
        super().__init__(message, details)
        self.selector = selector
        self.timeout = timeout


class ElementNotInteractableError(AutotestException):
    """Элемент не может быть взаимодействовать."""

    def __init__(self, selector: str, reason: str = None, details: str = None):
        reason_msg = f" ({reason})" if reason else ""
        message = f"Элемент '{selector}' неактивен{reason_msg}"
        super().__init__(message, details)
        self.selector = selector
        self.reason = reason


class ElementNotVisibleError(AutotestException):
    """Элемент не видим на странице."""

    def __init__(self, selector: str, details: str = None):
        message = f"Элемент '{selector}' не отображается"
        super().__init__(message, details)
        self.selector = selector


class NavigationError(AutotestException):
    """Ошибка навигации."""

    def __init__(self, expected_url: str, actual_url: str = None, details: str = None):
        url_msg = f" (получен: {actual_url})" if actual_url else ""
        message = f"Ошибка навигации. Ожидался URL: {expected_url}{url_msg}"
        super().__init__(message, details)
        self.expected_url = expected_url
        self.actual_url = actual_url


class TimeoutError(AutotestException):
    """Ошибка таймаута."""

    def __init__(self, operation: str, timeout: int, details: str = None):
        message = f"Таймаут операции '{operation}' ({timeout}ms)"
        super().__init__(message, details)
        self.operation = operation
        self.timeout = timeout


class LocatorNotFoundError(AutotestException):
    """Локатор не найден."""

    def __init__(self, locator_name: str, details: str = None):
        message = f"Локатор '{locator_name}' не найден"
        super().__init__(message, details)
        self.locator_name = locator_name


class ProjectNotFoundError(AutotestException):
    """Проект не найден."""

    def __init__(
        self, project_name: str, available_projects: list = None, details: str = None
    ):
        available_msg = (
            f" (доступны: {', '.join(available_projects)})"
            if available_projects
            else ""
        )
        message = f"Проект '{project_name}' не найден{available_msg}"
        super().__init__(message, details)
        self.project_name = project_name
        self.available_projects = available_projects or []


class EnvironmentError(AutotestException):
    """Ошибка окружения."""

    def __init__(
        self, environment: str, valid_environments: list = None, details: str = None
    ):
        valid_msg = (
            f" (доступны: {', '.join(valid_environments)})"
            if valid_environments
            else ""
        )
        message = f"Неверное окружение '{environment}'{valid_msg}"
        super().__init__(message, details)
        self.environment = environment
        self.valid_environments = valid_environments or []


class APIError(AutotestException):
    """Ошибка API."""

    def __init__(
        self,
        endpoint: str,
        status_code: int = None,
        response_text: str = None,
        details: str = None,
    ):
        status_msg = f" (статус: {status_code})" if status_code else ""
        message = f"Ошибка API для '{endpoint}'{status_msg}"
        super().__init__(message, details)
        self.endpoint = endpoint
        self.status_code = status_code
        self.response_text = response_text


class BrowserError(AutotestException):
    """Ошибка браузера."""

    def __init__(self, browser_type: str, operation: str, details: str = None):
        message = f"Ошибка браузера {browser_type} при операции '{operation}'"
        super().__init__(message, details)
        self.browser_type = browser_type
        self.operation = operation


class MobileDeviceError(AutotestException):
    """Ошибка мобильного устройства."""

    def __init__(self, device_type: str, operation: str, details: str = None):
        message = (
            f"Ошибка мобильного устройства {device_type} при операции '{operation}'"
        )
        super().__init__(message, details)
        self.device_type = device_type
        self.operation = operation


class TestDataError(AutotestException):
    """Ошибка тестовых данных."""

    def __init__(self, data_type: str, issue: str, details: str = None):
        message = f"Ошибка тестовых данных '{data_type}': {issue}"
        super().__init__(message, details)
        self.data_type = data_type
        self.issue = issue
