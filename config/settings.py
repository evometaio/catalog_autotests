"""
Основные настройки проекта автотестов.

Этот модуль содержит глобальные настройки проекта.
"""

import os
from dataclasses import dataclass
from typing import List, Optional

from dotenv import load_dotenv

from core.exceptions import ConfigurationError

# Загружаем переменные из .env файла
load_dotenv()


@dataclass
class BrowserConfig:
    """Конфигурация браузера."""

    name: str
    headless: bool = True
    timeout: int = 30000
    viewport_width: int = 1920
    viewport_height: int = 1080
    ignore_https_errors: bool = True
    args: List[str] = None

    def __post_init__(self):
        if self.args is None:
            self.args = []


@dataclass
class MobileConfig:
    """Конфигурация мобильного устройства."""

    device_type: str = "iPhone 13 Pro"
    viewport_width: int = 375
    viewport_height: int = 812
    device_scale_factor: int = 3
    has_touch: bool = True
    is_mobile: bool = True
    user_agent: str = (
        "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1"
    )


@dataclass
class TestConfig:
    """Конфигурация тестов."""

    default_timeout: int = 10000
    long_timeout: int = 15000
    short_timeout: int = 5000
    map_load_timeout: int = 20000
    max_retries: int = 3
    retry_delay: float = 1.0
    parallel_workers: Optional[int] = None
    max_failures: int = 0
    continue_on_collection_errors: bool = True


@dataclass
class ReportingConfig:
    """Конфигурация отчетности."""

    allure_results_dir: str = "reports/allure-results"
    allure_report_dir: str = "reports/allure-report"
    screenshots_dir: str = "reports/screenshots"
    logs_dir: str = "logs"
    generate_screenshots_on_failure: bool = True
    attach_page_source_on_failure: bool = True
    attach_console_logs: bool = True


@dataclass
class APIConfig:
    """Конфигурация API."""

    base_timeout: int = 30
    max_retries: int = 3
    retry_delay: float = 1.0
    verify_ssl: bool = True
    default_headers: dict = None

    def __post_init__(self):
        if self.default_headers is None:
            self.default_headers = {
                "Content-Type": "application/json",
                "Accept": "application/json",
            }


class Settings:
    """Основные настройки проекта."""

    def __init__(self):
        self._load_settings()

    def _load_settings(self) -> None:
        """Загружает настройки из переменных окружения."""

        # Конфигурация браузера
        self.browser = BrowserConfig(
            name=os.getenv("BROWSER", "chromium"),
            headless=os.getenv("HEADLESS", "true").lower() == "true",
            timeout=int(os.getenv("BROWSER_TIMEOUT", "30000")),
            viewport_width=int(os.getenv("VIEWPORT_WIDTH", "1920")),
            viewport_height=int(os.getenv("VIEWPORT_HEIGHT", "1080")),
            ignore_https_errors=os.getenv("IGNORE_HTTPS_ERRORS", "true").lower()
            == "true",
            args=self._parse_browser_args(os.getenv("BROWSER_ARGS", "")),
        )

        # Конфигурация мобильного устройства
        self.mobile = MobileConfig(
            device_type=os.getenv("MOBILE_DEVICE", "iPhone 13 Pro"),
            viewport_width=int(os.getenv("MOBILE_VIEWPORT_WIDTH", "375")),
            viewport_height=int(os.getenv("MOBILE_VIEWPORT_HEIGHT", "812")),
            device_scale_factor=int(os.getenv("MOBILE_SCALE_FACTOR", "3")),
            has_touch=os.getenv("MOBILE_HAS_TOUCH", "true").lower() == "true",
            is_mobile=os.getenv("MOBILE_IS_MOBILE", "true").lower() == "true",
            user_agent=os.getenv("MOBILE_USER_AGENT", MobileConfig.user_agent),
        )

        # Конфигурация тестов
        self.test = TestConfig(
            default_timeout=int(os.getenv("DEFAULT_TIMEOUT", "10000")),
            long_timeout=int(os.getenv("LONG_TIMEOUT", "15000")),
            short_timeout=int(os.getenv("SHORT_TIMEOUT", "5000")),
            map_load_timeout=int(os.getenv("MAP_LOAD_TIMEOUT", "20000")),
            max_retries=int(os.getenv("MAX_RETRIES", "3")),
            retry_delay=float(os.getenv("RETRY_DELAY", "1.0")),
            parallel_workers=int(os.getenv("PARALLEL_WORKERS", "0")) or None,
            max_failures=int(os.getenv("MAX_FAILURES", "0")),
            continue_on_collection_errors=os.getenv(
                "CONTINUE_ON_COLLECTION_ERRORS", "true"
            ).lower()
            == "true",
        )

        # Конфигурация отчетности
        self.reporting = ReportingConfig(
            allure_results_dir=os.getenv(
                "ALLURE_RESULTS_DIR", "reports/allure-results"
            ),
            allure_report_dir=os.getenv("ALLURE_REPORT_DIR", "reports/allure-report"),
            screenshots_dir=os.getenv("SCREENSHOTS_DIR", "reports/screenshots"),
            logs_dir=os.getenv("LOGS_DIR", "logs"),
            generate_screenshots_on_failure=os.getenv(
                "SCREENSHOTS_ON_FAILURE", "true"
            ).lower()
            == "true",
            attach_page_source_on_failure=os.getenv(
                "PAGE_SOURCE_ON_FAILURE", "true"
            ).lower()
            == "true",
            attach_console_logs=os.getenv("CONSOLE_LOGS", "true").lower() == "true",
        )

        # Конфигурация API
        self.api = APIConfig(
            base_timeout=int(os.getenv("API_TIMEOUT", "30")),
            max_retries=int(os.getenv("API_MAX_RETRIES", "3")),
            retry_delay=float(os.getenv("API_RETRY_DELAY", "1.0")),
            verify_ssl=os.getenv("API_VERIFY_SSL", "true").lower() == "true",
        )

        # Общие настройки
        self.project_name = os.getenv("PROJECT_NAME", "autotests")
        self.version = os.getenv("PROJECT_VERSION", "1.0.0")
        self.debug = os.getenv("DEBUG", "false").lower() == "true"
        self.verbose = os.getenv("VERBOSE", "false").lower() == "true"

    def _parse_browser_args(self, args_string: str) -> List[str]:
        """Парсит аргументы браузера из строки."""
        if not args_string:
            return []
        return [arg.strip() for arg in args_string.split(",") if arg.strip()]

    def validate(self) -> None:
        """Валидирует настройки."""
        errors = []

        # Проверяем браузер
        if self.browser.timeout <= 0:
            errors.append("Browser timeout должен быть положительным числом")

        if self.browser.viewport_width <= 0 or self.browser.viewport_height <= 0:
            errors.append("Viewport размеры должны быть положительными числами")

        # Проверяем тесты
        if self.test.default_timeout <= 0:
            errors.append("Default timeout должен быть положительным числом")

        if self.test.max_retries < 0:
            errors.append("Max retries не может быть отрицательным числом")

        # Проверяем API
        if self.api.base_timeout <= 0:
            errors.append("API timeout должен быть положительным числом")

        if errors:
            raise ConfigurationError(f"Ошибки конфигурации: {'; '.join(errors)}")

    def get_browser_args(self, browser_name: str) -> List[str]:
        """Получает аргументы для конкретного браузера."""
        base_args = self.browser.args.copy()

        if browser_name == "chromium":
            base_args.extend(
                [
                    "--no-sandbox",
                    "--disable-dev-shm-usage",
                    "--disable-gpu",
                    "--disable-web-security",
                    "--disable-features=VizDisplayCompositor",
                ]
            )
        elif browser_name == "firefox":
            # Firefox специфичные аргументы
            pass
        elif browser_name == "webkit":
            # WebKit специфичные аргументы
            pass

        return base_args


# Глобальный экземпляр настроек
settings = Settings()

# Валидируем настройки при импорте
try:
    settings.validate()
except ConfigurationError as e:
    print(f"Ошибка конфигурации: {e}")
    raise
