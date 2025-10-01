"""
Базовые утилиты для работы с локаторами.

Этот модуль содержит простые и эффективные утилиты для управления локаторами.
"""

from typing import Dict, Optional, Any
from dataclasses import dataclass
from datetime import datetime


@dataclass
class LocatorInfo:
    """Информация о локаторе."""

    selector: str
    description: str
    project: Optional[str] = None
    component: Optional[str] = None
    last_updated: str = None
    fallback: Optional[str] = None
    deprecated: bool = False
    replacement: Optional[str] = None


class LocatorRegistry:
    """Реестр локаторов для простого доступа."""

    def __init__(self):
        """Инициализация реестра."""
        self._locators: Dict[str, LocatorInfo] = {}
        self._by_project: Dict[str, Dict[str, LocatorInfo]] = {}
        self._by_component: Dict[str, Dict[str, LocatorInfo]] = {}

    def add_locator(
        self,
        name: str,
        selector: str,
        description: str,
        project: Optional[str] = None,
        component: Optional[str] = None,
        fallback: Optional[str] = None,
    ) -> None:
        """Добавить локатор в реестр."""

        locator_info = LocatorInfo(
            selector=selector,
            description=description,
            project=project,
            component=component,
            last_updated=datetime.now().isoformat(),
            fallback=fallback,
        )

        self._locators[name] = locator_info

        # Группировка по проектам
        if project:
            if project not in self._by_project:
                self._by_project[project] = {}
            self._by_project[project][name] = locator_info

        # Группировка по компонентам
        if component:
            if component not in self._by_component:
                self._by_component[component] = {}
            self._by_component[component][name] = locator_info

    def get_locator(self, name: str, use_fallback: bool = False) -> str:
        """Получить селектор локатора."""

        if name not in self._locators:
            raise KeyError(f"Локатор '{name}' не найден")

        locator_info = self._locators[name]

        if locator_info.deprecated and locator_info.replacement:
            print(
                f"⚠️ Локатор '{name}' устарел. Используйте '{locator_info.replacement}'"
            )

        if use_fallback and locator_info.fallback:
            return locator_info.fallback

        return locator_info.selector

    def get_project_locators(self, project: str) -> Dict[str, str]:
        """Получить все локаторы проекта."""

        if project not in self._by_project:
            return {}

        return {name: info.selector for name, info in self._by_project[project].items()}

    def get_component_locators(self, component: str) -> Dict[str, str]:
        """Получить все локаторы компонента."""

        if component not in self._by_component:
            return {}

        return {
            name: info.selector for name, info in self._by_component[component].items()
        }

    def list_locators(self) -> Dict[str, str]:
        """Получить все локаторы."""

        return {name: info.selector for name, info in self._locators.items()}

    def search_locators(self, query: str) -> Dict[str, str]:
        """Поиск локаторов по названию или описанию."""

        result = {}
        query_lower = query.lower()

        for name, info in self._locators.items():
            if query_lower in name.lower() or query_lower in info.description.lower():
                result[name] = info.selector

        return result

    def mark_deprecated(self, name: str, replacement: str) -> None:
        """Пометить локатор как устаревший."""

        if name in self._locators:
            self._locators[name].deprecated = True
            self._locators[name].replacement = replacement


# Глобальный реестр локаторов
locator_registry = LocatorRegistry()
