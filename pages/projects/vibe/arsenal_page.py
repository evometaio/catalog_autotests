"""Страница проекта Arsenal (Vibe)."""

from playwright.sync_api import Page

from locators.vibe.arsenal_locators import ArsenalLocators

from ..qube.qube_base_page import QubeBasePage


class ArsenalPage(QubeBasePage):
    """
    Страница проекта Arsenal (Vibe).

    Наследует от QubeBasePage, так как проект аналогичен Cubix:
    сразу в catalog2d все аппарты и есть map.
    """

    def __init__(self, page: Page, url: str = None):
        """
        Инициализация Arsenal страницы.

        Args:
            page: Playwright Page объект
            url: URL страницы
        """
        # Инициализируем с project_name="arsenal" и новыми локаторами
        super().__init__(page, "arsenal", url, ArsenalLocators)

    def open(self, path: str = "", route_type: str = None):
        """
        Открыть страницу Arsenal.

        Args:
            path: Дополнительный путь к базовому URL
            route_type: Игнорируется для Arsenal (нет agent/client routes, только map)
        """
        # Для Arsenal игнорируем route_type, так как нет agent/client routes
        url = self.base_url

        # Добавляем дополнительный путь если есть
        if path:
            url = f"{url.rstrip('/')}/{path.lstrip('/')}"

        self.page.goto(url)
        self.wait_for_page_load()

        # Принудительно сбрасываем масштаб страницы
        self.page.evaluate("document.body.style.zoom = '1'")
        self.page.evaluate("document.documentElement.style.zoom = '1'")
