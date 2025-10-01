"""
Конфигурация окружений для автотестов.

Этот модуль содержит настройки для различных окружений (dev, prod).
"""

import os
from dataclasses import dataclass
from typing import Dict, Optional

from core.exceptions import EnvironmentError


@dataclass
class EnvironmentConfig:
    """Конфигурация окружения."""

    name: str
    base_url: str
    agent_url: str
    client_url: str
    capstone_map_url: str
    wellcube_map_url: str
    timeout: int = 30
    verify_ssl: bool = True
    headless: bool = True
    api_key: Optional[str] = None

    def validate(self) -> None:
        """Валидирует конфигурацию окружения."""
        if not self.name:
            raise EnvironmentError("", "Имя окружения не может быть пустым")

        urls = [
            ("base_url", self.base_url),
            ("agent_url", self.agent_url),
            ("client_url", self.client_url),
            ("capstone_map_url", self.capstone_map_url),
            ("wellcube_map_url", self.wellcube_map_url),
        ]

        for url_name, url in urls:
            if not url or not url.startswith(("http://", "https://")):
                raise EnvironmentError(self.name, f"Неверный URL для {url_name}: {url}")

        if self.timeout <= 0:
            raise EnvironmentError(
                self.name, f"Таймаут должен быть положительным числом: {self.timeout}"
            )


class EnvironmentManager:
    """Менеджер окружений."""

    VALID_ENVIRONMENTS = ["dev", "prod"]

    def __init__(self):
        self._environments: Dict[str, EnvironmentConfig] = {}
        self._load_environments()

    def _load_environments(self) -> None:
        """Загружает конфигурации окружений из переменных окружения."""

        # DEV окружение
        dev_config = EnvironmentConfig(
            name="dev",
            base_url=os.getenv("DEV_BASE_URL", "https://qube-dev-next.evometa.io/map"),
            agent_url=os.getenv(
                "DEV_AGENT_BASE_URL", "https://qube-dev-next.evometa.io/agent/map"
            ),
            client_url=os.getenv(
                "DEV_CLIENT_BASE_URL", "https://qube-dev-next.evometa.io/client/map"
            ),
            capstone_map_url=os.getenv(
                "DEV_CAPSTONE_BASE_URL", "https://capstone-dev.evometa.io/map"
            ),
            wellcube_map_url=os.getenv(
                "DEV_WELLCUBE_BASE_URL", "https://catalog-dev.evometa.io/wellcube/map"
            ),
            timeout=int(os.getenv("DEV_TIMEOUT", "30")),
            verify_ssl=os.getenv("DEV_VERIFY_SSL", "true").lower() == "true",
            headless=os.getenv("DEV_HEADLESS", "true").lower() == "true",
            api_key=os.getenv("DEV_API_KEY"),
        )

        # PROD окружение
        prod_config = EnvironmentConfig(
            name="prod",
            base_url=os.getenv("PROD_BASE_URL", "https://virtualtours.qbd.ae/map"),
            agent_url=os.getenv(
                "AGENT_PROD_BASE_URL", "https://virtualtours.qbd.ae/agent/map"
            ),
            client_url=os.getenv(
                "CLIENT_PROD_BASE_URL", "https://virtualtours.qbd.ae/client/map"
            ),
            capstone_map_url=os.getenv(
                "CAPSTONE_PROD_BASE_URL", "https://3dtours.peylaa-phuket.com/map"
            ),
            wellcube_map_url=os.getenv(
                "WELLCUBE_PROD_BASE_URL", "https://catalog.evometa.io/wellcube/map"
            ),
            timeout=int(os.getenv("PROD_TIMEOUT", "30")),
            verify_ssl=os.getenv("PROD_VERIFY_SSL", "true").lower() == "true",
            headless=os.getenv("PROD_HEADLESS", "true").lower() == "true",
            api_key=os.getenv("PROD_API_KEY"),
        )

        self._environments["dev"] = dev_config
        self._environments["prod"] = prod_config

    def get_environment(self, name: str = None) -> EnvironmentConfig:
        """
        Получить конфигурацию окружения.

        Args:
            name: Имя окружения (если не указано, берется из TEST_ENVIRONMENT)

        Returns:
            Конфигурация окружения

        Raises:
            EnvironmentError: Если окружение не найдено или неверно
        """
        if name is None:
            name = os.getenv("TEST_ENVIRONMENT", "prod")

        if name not in self.VALID_ENVIRONMENTS:
            raise EnvironmentError(
                name,
                self.VALID_ENVIRONMENTS,
                f"Поддерживаемые окружения: {', '.join(self.VALID_ENVIRONMENTS)}",
            )

        config = self._environments.get(name)
        if not config:
            raise EnvironmentError(
                name,
                self.VALID_ENVIRONMENTS,
                f"Конфигурация для окружения '{name}' не найдена",
            )

        # Валидируем конфигурацию
        config.validate()

        return config

    def get_all_environments(self) -> Dict[str, EnvironmentConfig]:
        """Получить все доступные окружения."""
        return self._environments.copy()

    def validate_current_environment(self) -> None:
        """Валидирует текущее окружение."""
        current_env = os.getenv("TEST_ENVIRONMENT", "prod")
        self.get_environment(current_env)


# Глобальный экземпляр менеджера окружений
environment_manager = EnvironmentManager()
