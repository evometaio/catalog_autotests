"""
Локаторы для компонентов.

Этот модуль предоставляет доступ к локаторам различных компонентов.
"""

from .map import map_locators
from .mobile import mobile_locators
from .modals import modal_locators

# Экспорт всех компонентных локаторов
__all__ = ["map_locators", "mobile_locators", "modal_locators"]
