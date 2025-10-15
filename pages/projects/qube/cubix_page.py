"""Страница проекта Cubix."""

from playwright.sync_api import Page

from .qube_base_page import QubeBasePage
from locators.qube.cubix_locators import CubixLocators


class CubixPage(QubeBasePage):
    """
    Страница проекта Cubix.
    
    Наследует от QubeBasePage. Вся общая функциональность Qube уже есть в базовом классе.
    """

    def __init__(self, page: Page, url: str = None):
        """
        Инициализация Cubix страницы.
        
        Args:
            page: Playwright Page объект
            url: URL страницы
        """
        # Инициализируем с project_name="cubix" и новыми локаторами
        super().__init__(page, "cubix", url, CubixLocators)

    # Специфичные методы для Cubix могут быть добавлены здесь
    # Сейчас их нет, вся функциональность в QubeBasePage
