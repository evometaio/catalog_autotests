"""Страница проекта Arisha."""

from playwright.sync_api import Page

from locators.qube.arisha_locators import ArishaLocators

from .qube_base_page import QubeBasePage


class ArishaPage(QubeBasePage):
    """
    Страница проекта Arisha.

    Наследует от QubeBasePage. Вся общая функциональность Qube уже есть в базовом классе.
    """

    def __init__(self, page: Page, url: str = None):
        """
        Инициализация Arisha страницы.

        Args:
            page: Playwright Page объект
            url: URL страницы
        """
        # Инициализируем с project_name="arisha" и новыми локаторами
        super().__init__(page, "arisha", url, ArishaLocators)

    # Специфичные методы для Arisha могут быть добавлены здесь
    # Сейчас их нет, вся функциональность в QubeBasePage
