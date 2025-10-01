"""
Декораторы для автотестов.

Этот модуль содержит полезные декораторы для тестов и page objects.
"""

import time
from functools import wraps
from typing import Any, Callable, Optional, Type, Union

import allure

from config.settings import settings
from core.exceptions import TimeoutError as CustomTimeoutError
from utils.logger import get_logger

logger = get_logger(__name__)


def retry_on_failure(
    max_attempts: int = None,
    delay: float = None,
    exceptions: tuple = None,
    backoff_factor: float = 1.0,
):
    """
    Декоратор для повторных попыток при неудаче.

    Args:
        max_attempts: Максимальное количество попыток
        delay: Задержка между попытками в секундах
        exceptions: Кортеж исключений, при которых нужно повторять
        backoff_factor: Коэффициент увеличения задержки

    Returns:
        Декорированная функция
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            attempts = max_attempts or settings.test.max_retries
            wait_time = delay or settings.test.retry_delay
            exception_types = exceptions or (Exception,)

            last_exception = None

            for attempt in range(attempts):
                try:
                    with allure.step(f"Попытка {attempt + 1} из {attempts}"):
                        result = func(*args, **kwargs)
                        if attempt > 0:
                            logger.info(
                                f"Функция {func.__name__} выполнена успешно с попытки {attempt + 1}"
                            )
                        return result

                except exception_types as e:
                    last_exception = e

                    if attempt == attempts - 1:
                        logger.error(
                            f"Функция {func.__name__} не выполнена после {attempts} попыток: {e}"
                        )
                        raise

                    logger.warning(
                        f"Попытка {attempt + 1} неудачна для {func.__name__}: {e}"
                    )

                    # Увеличиваем задержку с каждым повтором
                    current_delay = wait_time * (backoff_factor**attempt)
                    time.sleep(current_delay)

            # Этот код не должен выполниться, но на всякий случай
            if last_exception:
                raise last_exception

        return wrapper

    return decorator


def timeout(seconds: float):
    """
    Декоратор для установки таймаута на выполнение функции.

    Args:
        seconds: Таймаут в секундах

    Returns:
        Декорированная функция
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            import signal

            def timeout_handler(signum, frame):
                raise CustomTimeoutError(func.__name__, int(seconds * 1000))

            # Устанавливаем обработчик сигнала
            old_handler = signal.signal(signal.SIGALRM, timeout_handler)
            signal.alarm(int(seconds))

            try:
                result = func(*args, **kwargs)
                return result
            finally:
                # Восстанавливаем старый обработчик
                signal.alarm(0)
                signal.signal(signal.SIGALRM, old_handler)

        return wrapper

    return decorator


def log_execution_time(func: Callable) -> Callable:
    """
    Декоратор для логирования времени выполнения функции.

    Returns:
        Декорированная функция
    """

    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        start_time = time.time()

        try:
            result = func(*args, **kwargs)
            execution_time = time.time() - start_time
            logger.info(
                f"Функция {func.__name__} выполнена за {execution_time:.2f} секунд"
            )
            return result
        except Exception as e:
            execution_time = time.time() - start_time
            logger.error(
                f"Функция {func.__name__} завершилась с ошибкой за {execution_time:.2f} секунд: {e}"
            )
            raise

    return wrapper


def allure_step(step_name: str = None):
    """
    Декоратор для создания Allure шагов.

    Args:
        step_name: Название шага (если не указано, используется имя функции)

    Returns:
        Декорированная функция
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            name = step_name or func.__name__.replace("_", " ").title()

            with allure.step(name):
                return func(*args, **kwargs)

        return wrapper

    return decorator


def skip_if_condition(condition: Callable, reason: str = "Условие не выполнено"):
    """
    Декоратор для условного пропуска тестов.

    Args:
        condition: Функция, возвращающая True если тест нужно пропустить
        reason: Причина пропуска

    Returns:
        Декорированная функция
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            if condition():
                import pytest

                pytest.skip(reason)
            return func(*args, **kwargs)

        return wrapper

    return decorator


def validate_input(**validators):
    """
    Декоратор для валидации входных параметров функции.

    Args:
        **validators: Словарь валидаторов для параметров

    Returns:
        Декорированная функция
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            import inspect

            # Получаем сигнатуру функции
            sig = inspect.signature(func)
            bound_args = sig.bind(*args, **kwargs)
            bound_args.apply_defaults()

            # Валидируем каждый параметр
            for param_name, validator in validators.items():
                if param_name in bound_args.arguments:
                    value = bound_args.arguments[param_name]
                    if not validator(value):
                        raise ValueError(
                            f"Неверное значение для параметра '{param_name}': {value}"
                        )

            return func(*args, **kwargs)

        return wrapper

    return decorator


def cache_result(func: Callable) -> Callable:
    """
    Декоратор для кеширования результата функции.

    Returns:
        Декорированная функция
    """
    cache = {}

    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        # Создаем ключ кеша из аргументов
        cache_key = str(args) + str(sorted(kwargs.items()))

        if cache_key in cache:
            logger.debug(f"Возвращаем кешированный результат для {func.__name__}")
            return cache[cache_key]

        result = func(*args, **kwargs)
        cache[cache_key] = result

        logger.debug(f"Результат {func.__name__} закеширован")
        return result

    return wrapper


def deprecated(reason: str = "Функция устарела"):
    """
    Декоратор для пометки устаревших функций.

    Args:
        reason: Причина устаревания

    Returns:
        Декорированная функция
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            logger.warning(f"Используется устаревшая функция {func.__name__}: {reason}")
            return func(*args, **kwargs)

        return wrapper

    return decorator
