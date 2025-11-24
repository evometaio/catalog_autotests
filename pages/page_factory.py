"""Фабрика для создания page objects."""

from playwright.sync_api import Page

from conftest import _get_urls_by_environment
from locators.base_locators import BaseLocators
from pages.base_page import BasePage


class PageFactory:
    """Фабрика для создания page objects."""

    @staticmethod
    def get_page_by_project(page: Page, project_name: str):
        """
        Получить page object для конкретного проекта.

        Args:
            page: Playwright Page объект
            project_name: Название проекта (arisha, elire, cubix, peylaa, tranquil)

        Returns:
            Соответствующий page object проекта
        """
        project_name_lower = project_name.lower()

        # Импортируем нужный класс динамически
        if project_name_lower == "arisha":
            from pages.projects.qube.arisha_page import ArishaPage

            return ArishaPage(page)
        elif project_name_lower == "elire":
            from pages.projects.qube.elire_page import ElirePage

            return ElirePage(page)
        elif project_name_lower == "cubix":
            from pages.projects.qube.cubix_page import CubixPage

            return CubixPage(page)
        elif project_name_lower == "peylaa":
            from pages.projects.capstone.peylaa_page import PeylaaPage

            return PeylaaPage(page)
        elif project_name_lower == "tranquil":
            from pages.projects.wellcube.tranquil_page import TranquilPage

            return TranquilPage(page)
        elif project_name_lower == "mark":
            from pages.projects.lsr.mark_page import MarkPage

            urls = _get_urls_by_environment()
            return MarkPage(page, urls["lsr_mark"])
        elif project_name_lower == "arsenal":
            from pages.projects.vibe.arsenal_page import ArsenalPage

            urls = _get_urls_by_environment()
            return ArsenalPage(page, urls["vibe_arsenal"])
        else:
            raise ValueError(f"Неизвестный проект: {project_name}")

    @staticmethod
    def get_page_by_developer(page: Page, developer_type: str):
        """
        Получить базовую page для типа застройщика.

        Args:
            page: Playwright Page объект
            developer_type: Тип застройщика ('qube', 'wellcube', 'capstone')

        Returns:
            BasePage с правильными локаторами
        """
        urls = _get_urls_by_environment()

        if developer_type == "qube":
            return BasePage(page, urls["map"], BaseLocators)
        elif developer_type == "capstone":
            from pages.projects.capstone.peylaa_page import PeylaaPage

            return PeylaaPage(page)
        elif developer_type == "wellcube":
            from pages.projects.wellcube.tranquil_page import TranquilPage

            return TranquilPage(page)
        elif developer_type == "lsr":
            from pages.projects.lsr.mark_page import MarkPage

            urls = _get_urls_by_environment()
            return MarkPage(page, urls["lsr_mark"])
        elif developer_type == "vibe":
            from pages.projects.vibe.arsenal_page import ArsenalPage

            urls = _get_urls_by_environment()
            return ArsenalPage(page, urls["vibe_arsenal"])
        else:
            raise ValueError(f"Неизвестный тип застройщика: {developer_type}")

    # Алиас для обратной совместимости
    @staticmethod
    def get_page_object(page: Page, developer_type: str):
        """Deprecated: используйте get_page_by_developer()."""
        return PageFactory.get_page_by_developer(page, developer_type)
