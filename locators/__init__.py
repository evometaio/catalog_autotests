"""
Оптимизированная система локаторов.

Этот модуль предоставляет простой и понятный доступ ко всем локаторам проекта.
"""

# Импортируем все локаторы проектов
from .projects import (
    qube_locators,
    wellcube_locators,
    capstone_locators,
    common_locators,
)

# Импортируем все компонентные локаторы
from .components import map_locators, mobile_locators, modal_locators

# Импортируем базовые утилиты
from .base import locator_registry, LocatorRegistry


# Главный объект для доступа ко всем локаторам
class Locators:
    """Главный класс для доступа ко всем локаторам."""

    def __init__(self):
        """Инициализация главного объекта локаторов."""
        self.qube = qube_locators
        self.wellcube = wellcube_locators
        self.capstone = capstone_locators
        self.common = common_locators

        self.map = map_locators
        self.mobile = mobile_locators
        self.modal = modal_locators

        self.registry = locator_registry

    def get(self, name: str, use_fallback: bool = False) -> str:
        """Получить локатор по имени из любого модуля."""
        return self.registry.get_locator(name, use_fallback)

    def search(self, query: str) -> dict:
        """Поиск локаторов по названию или описанию."""
        return self.registry.search_locators(query)

    def list_all(self) -> dict:
        """Получить все доступные локаторы."""
        return self.registry.list_locators()

    def get_project_locators(self, project: str) -> dict:
        """Получить все локаторы проекта."""
        return self.registry.get_project_locators(project)

    def get_component_locators(self, component: str) -> dict:
        """Получить все локаторы компонента."""
        return self.registry.get_component_locators(component)


# Создаем главный объект
locators = Locators()

# Экспортируем все важные объекты
__all__ = [
    "locators",
    "locator_registry",
    "LocatorRegistry",
    "qube_locators",
    "wellcube_locators",
    "capstone_locators",
    "common_locators",
    "map_locators",
    "mobile_locators",
    "modal_locators",
]
