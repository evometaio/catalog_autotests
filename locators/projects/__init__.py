"""
Локаторы для всех проектов.

Этот модуль предоставляет простой доступ к локаторам всех проектов.
"""

from .qube import qube_locators
from .wellcube import wellcube_locators
from .capstone import capstone_locators
from .common import common_locators

# Экспорт всех локаторов
__all__ = ["qube_locators", "wellcube_locators", "capstone_locators", "common_locators"]
