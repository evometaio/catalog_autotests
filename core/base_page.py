"""
Базовый класс для всех страниц с улучшенной архитектурой.

Этот модуль содержит базовые классы и миксины для page objects.
"""

import time
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union

import allure
from playwright.sync_api import Locator, Page, expect

from config.settings import settings
from core.decorators import allure_step, log_execution_time, retry_on_failure
from core.exceptions import (
    ElementNotFoundError,
    ElementNotInteractableError,
    ElementNotVisibleError,
    NavigationError,
)
from core.exceptions import TimeoutError as CustomTimeoutError
from utils.logger import get_logger

logger = get_logger(__name__)


class BasePage(ABC):
    """Базовый класс для всех страниц."""

    def __init__(self, page: Page, base_url: str, locators_class: type) -> None:
        """
        Инициализация базовой страницы.

        Args:
            page: Playwright Page объект
            base_url: Базовый URL страницы
            locators_class: Класс локаторов
        """
        self.page = page
        self.base_url = base_url.rstrip("/")
        self.locators = locators_class()

        # Инициализируем миксины
        self._navigation = NavigationMixin(self)
        self._interaction = InteractionMixin(self)
        self._validation = ValidationMixin(self)
        self._waiting = WaitingMixin(self)

        # URL-ы для навигации
        if "/map" in base_url:
            self.project_url_template = base_url.replace(
                "/map", "/project/{project}/area"
            )
            self.map_url = base_url

    # Делегируем методы к миксинам
    def open(self, path: str = "", route_type: str = None) -> None:
        """Открыть страницу."""
        return self._navigation.open(path, route_type)

    def click(self, selector: str, timeout: Optional[int] = None) -> None:
        """Кликнуть по элементу."""
        return self._interaction.click(selector, timeout)

    def fill(self, selector: str, text: str, timeout: Optional[int] = None) -> None:
        """Заполнить поле."""
        return self._interaction.fill(selector, text, timeout)

    def get_text(self, selector: str, timeout: Optional[int] = None) -> str:
        """Получить текст элемента."""
        return self._interaction.get_text(selector, timeout)

    def is_visible(self, selector: str, timeout: Optional[int] = None) -> bool:
        """Проверить видимость элемента."""
        return self._validation.is_visible(selector, timeout)

    def expect_visible(self, selector: str, timeout: Optional[int] = None) -> None:
        """Ожидать видимости элемента."""
        return self._validation.expect_visible(selector, timeout)

    def wait_for_element(self, selector: str, timeout: Optional[int] = None) -> Locator:
        """Ожидать появления элемента."""
        return self._waiting.wait_for_element(selector, timeout)

    def wait_for_page_load(self) -> None:
        """Ожидать загрузки страницы."""
        return self._waiting.wait_for_page_load()

    def get_current_url(self) -> str:
        """Получить текущий URL."""
        return self.page.url

    def get_project_url(self, project_name: str, page_type: str = "catalog_2d") -> str:
        """Получить URL для конкретного проекта и типа страницы."""
        return self._navigation.get_project_url(project_name, page_type)


class NavigationMixin:
    """Миксин для навигационных методов."""

    def __init__(self, page_object: BasePage):
        self.page_object = page_object

    @allure_step("Открыть страницу")
    def open(self, path: str = "", route_type: str = None) -> None:
        """
        Открыть страницу.

        Args:
            path: Дополнительный путь к базовому URL
            route_type: Тип роута для проверки - "client", "agent" или "map"
        """
        url = (
            f"{self.page_object.base_url}/{path.lstrip('/')}"
            if path
            else self.page_object.base_url
        )

        logger.info(f"Открываем страницу: {url}")
        self.page_object.page.goto(url)
        self.page_object.wait_for_page_load()

        # Принудительно сбрасываем масштаб страницы
        self.page_object.page.evaluate("document.body.style.zoom = '1'")
        self.page_object.page.evaluate("document.documentElement.style.zoom = '1'")

        current_url = self.page_object.get_current_url()
        if url not in current_url:
            raise NavigationError(url, current_url, "Не удалось открыть страницу")

        # Проверяем тип роута, если указан
        if route_type:
            self._validate_route_type(current_url, route_type)

    def _validate_route_type(self, current_url: str, route_type: str) -> None:
        """Валидирует тип роута."""
        if route_type == "client" and "client" not in current_url:
            raise NavigationError(
                f"*/client/*", current_url, "Не открылась клиентская страница"
            )
        elif route_type == "agent" and "agent" not in current_url:
            raise NavigationError(
                f"*/agent/*", current_url, "Не открылась агентская страница"
            )
        elif route_type == "map" and "map" not in current_url:
            raise NavigationError(f"*/map*", current_url, "Не открылась страница карты")

    def get_project_url(self, project_name: str, page_type: str = "catalog_2d") -> str:
        """
        Получить URL для конкретного проекта и типа страницы.

        Args:
            project_name: Название проекта (arisha, cubix, elire, peylaa, tranquil)
            page_type: Тип страницы (catalog_2d, area, map)

        Returns:
            str: URL для проекта
        """
        from config.environments import environment_manager

        env_config = environment_manager.get_environment()
        project_name_lower = project_name.lower()

        # Проверяем валидность типа страницы
        if page_type not in self.page_object.locators.PAGE_TYPES:
            raise ValueError(f"Неизвестный тип страницы: {page_type}")

        # Определяем базовый URL в зависимости от проекта
        if project_name_lower in ["arisha", "cubix", "elire"]:
            # Qube проекты
            base_url = env_config.base_url.replace("/map", "")
            map_url = env_config.base_url
        elif project_name_lower == "peylaa":
            # Capstone проект
            base_url = env_config.capstone_map_url.replace("/map", "")
            map_url = env_config.capstone_map_url
        elif project_name_lower == "tranquil":
            # Wellcube проект
            base_url = env_config.wellcube_map_url.replace("/map", "")
            map_url = env_config.wellcube_map_url
        else:
            raise ValueError(f"Неизвестный проект: {project_name}")

        # Формируем полный URL
        if page_type == "catalog_2d":
            return f"{base_url}/project/{project_name_lower}/catalog_2d"
        elif page_type == "area":
            return f"{base_url}/project/{project_name_lower}/area"
        elif page_type == "map":
            return map_url


class InteractionMixin:
    """Миксин для методов взаимодействия с элементами."""

    def __init__(self, page_object: BasePage):
        self.page_object = page_object

    @retry_on_failure(max_attempts=2)
    @allure_step("Кликнуть по элементу")
    def click(self, selector: str, timeout: Optional[int] = None) -> None:
        """
        Кликнуть по элементу.

        Args:
            selector: Селектор элемента
            timeout: Таймаут ожидания
        """
        if not selector or not isinstance(selector, str):
            raise ValueError("Selector должен быть непустой строкой")

        element = self.page_object.wait_for_element(selector, timeout)

        if not element.is_enabled():
            raise ElementNotInteractableError(
                selector, "элемент неактивен", "Баг в UI - элемент заблокирован"
            )

        logger.debug(f"Кликаем по элементу: {selector}")
        element.click()

    @allure_step("Заполнить поле")
    def fill(self, selector: str, text: str, timeout: Optional[int] = None) -> None:
        """
        Заполнить поле.

        Args:
            selector: Селектор поля
            text: Текст для заполнения
            timeout: Таймаут ожидания
        """
        if not text or not isinstance(text, str):
            raise ValueError("Text должен быть непустой строкой")

        element = self.page_object.wait_for_element(selector, timeout)

        if not element.is_enabled():
            raise ElementNotInteractableError(
                selector, "поле неактивно", "Баг в UI - поле заблокировано"
            )

        logger.debug(f"Заполняем поле {selector} текстом: {text}")
        element.fill(text)

    @allure_step("Получить текст элемента")
    def get_text(self, selector: str, timeout: Optional[int] = None) -> str:
        """
        Получить текст элемента.

        Args:
            selector: Селектор элемента
            timeout: Таймаут ожидания

        Returns:
            Текст элемента
        """
        element = self.page_object.wait_for_element(selector, timeout)
        text = element.text_content()
        logger.debug(f"Получен текст из {selector}: {text}")
        return text or ""


class ValidationMixin:
    """Миксин для методов проверок."""

    def __init__(self, page_object: BasePage):
        self.page_object = page_object

    def is_visible(self, selector: str, timeout: Optional[int] = None) -> bool:
        """
        Проверить видимость элемента.

        Args:
            selector: Селектор элемента
            timeout: Таймаут ожидания

        Returns:
            True если элемент видим
        """
        try:
            self.page_object.wait_for_element(selector, timeout)
            return True
        except (ElementNotFoundError, CustomTimeoutError):
            return False

    @allure_step("Проверить видимость элемента")
    def expect_visible(self, selector: str, timeout: Optional[int] = None) -> None:
        """
        Ожидать видимости элемента.

        Args:
            selector: Селектор элемента
            timeout: Таймаут ожидания
        """
        element = self.page_object.wait_for_element(selector, timeout)

        if not element.is_visible():
            raise ElementNotVisibleError(selector, "Элемент не отображается - баг в UI")


class WaitingMixin:
    """Миксин для методов ожидания."""

    def __init__(self, page_object: BasePage):
        self.page_object = page_object

    @log_execution_time
    def wait_for_element(self, selector: str, timeout: Optional[int] = None) -> Locator:
        """
        Ожидать появления элемента.

        Args:
            selector: Селектор элемента
            timeout: Таймаут ожидания

        Returns:
            Locator объект
        """
        if timeout is None:
            timeout = settings.test.default_timeout

        element = self.page_object.page.locator(selector)

        try:
            element.wait_for(state="visible", timeout=timeout)
            logger.debug(f"Элемент найден: {selector}")
            return element
        except Exception as e:
            raise ElementNotFoundError(
                selector, timeout, f"Элемент не найден за {timeout}ms: {e}"
            )

    def wait_for_page_load(self) -> None:
        """Ожидать загрузки страницы."""
        logger.debug("Ожидаем загрузки страницы")
        self.page_object.page.wait_for_load_state("domcontentloaded")

    def wait_for_timeout(self, timeout: int) -> None:
        """
        Ждать указанное количество миллисекунд.

        Args:
            timeout: Таймаут в миллисекундах
        """
        logger.debug(f"Ожидаем {timeout}ms")
        self.page_object.page.wait_for_timeout(timeout)


class PageObjectFactory:
    """Фабрика для создания page objects."""

    @staticmethod
    def create_page_object(
        page: Page, page_type: str, project: Optional[str] = None
    ) -> BasePage:
        """
        Создать page object для указанного типа страницы.

        Args:
            page: Playwright Page объект
            page_type: Тип страницы (map, agent, client, project)
            project: Название проекта (для project страниц)

        Returns:
            Соответствующий page object
        """
        from config.environments import environment_manager
        from locators.project_locators import (
            CapstonePageLocators,
            QubeLocators,
            WellcubePageLocators,
        )

        env_config = environment_manager.get_environment()

        if page_type == "map":
            if project == "peylaa":
                from pages.capstone.capstone_pages import CapstonePages

                return CapstonePages(page, env_config.capstone_map_url)
            elif project == "tranquil":
                from pages.wellcube.wellcube_pages import WellcubePages

                return WellcubePages(page, env_config.wellcube_map_url)
            else:
                return BasePage(page, env_config.base_url, QubeLocators)

        elif page_type == "agent":
            from pages.qube.agent_page import AgentPage

            return AgentPage(page, env_config.agent_url)

        elif page_type == "client":
            from pages.qube.client_page import ClientPage

            return ClientPage(page, env_config.client_url)

        else:
            raise ValueError(f"Неизвестный тип страницы: {page_type}")
