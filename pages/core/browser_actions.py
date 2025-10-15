"""Обёртки над Playwright API для взаимодействия с браузером."""

from playwright.sync_api import Locator, Page


class BrowserActions:
    """
    Класс для взаимодействия с браузером.

    Ответственность:
    - Обёртки над Playwright методами
    - Унифицированная обработка ошибок
    - Базовые действия (click, fill, wait, etc.)
    """

    DEFAULT_TIMEOUT = 10000

    def __init__(self, page: Page):
        """
        Инициализация.

        Args:
            page: Playwright Page объект
        """
        self.page = page

    def wait_for_element(self, selector: str, timeout: int = None) -> Locator:
        """
        Ожидать появления элемента.

        Args:
            selector: CSS селектор элемента
            timeout: Таймаут ожидания (мс)

        Returns:
            Locator объект

        Raises:
            AssertionError: Если элемент не найден
        """
        if timeout is None:
            timeout = self.DEFAULT_TIMEOUT

        element = self.page.locator(selector)

        try:
            element.wait_for(state="visible", timeout=timeout)
            return element
        except TimeoutError:
            raise AssertionError(f"Элемент '{selector}' не найден за {timeout}ms.")

    def click(self, selector: str, timeout: int = None, **kwargs):
        """
        Кликнуть по элементу.

        Args:
            selector: CSS селектор элемента
            timeout: Таймаут ожидания
            **kwargs: Дополнительные параметры для click()
        """
        element = self.wait_for_element(selector, timeout)
        assert element.is_enabled(), f"Элемент {selector} неактивен - баг в UI"
        element.click(**kwargs)

    def fill(self, selector: str, text: str, timeout: int = None):
        """
        Заполнить поле ввода.

        Args:
            selector: CSS селектор поля
            text: Текст для ввода
            timeout: Таймаут ожидания
        """
        element = self.wait_for_element(selector, timeout)
        element.fill(text)

    def get_text(self, selector: str, timeout: int = None) -> str:
        """
        Получить текст элемента.

        Args:
            selector: CSS селектор элемента
            timeout: Таймаут ожидания

        Returns:
            Текстовое содержимое элемента
        """
        element = self.wait_for_element(selector, timeout)
        return element.text_content()

    def is_visible(self, selector: str, timeout: int = None) -> bool:
        """
        Проверить видимость элемента.

        Args:
            selector: CSS селектор элемента
            timeout: Таймаут ожидания

        Returns:
            True если элемент виден, иначе False
        """
        try:
            self.wait_for_element(selector, timeout)
            return True
        except:
            return False

    def expect_visible(self, selector: str, timeout: int = None):
        """
        Ожидать видимости элемента.

        Args:
            selector: CSS селектор
            timeout: Таймаут ожидания
        """
        element = self.wait_for_element(selector, timeout)
        assert element.is_visible(), f"Элемент {selector} не отображается - баг в UI"

    def wait_for_timeout(self, timeout: int):
        """
        Ждать указанное количество миллисекунд.

        Args:
            timeout: Время ожидания в миллисекундах
        """
        self.page.wait_for_timeout(timeout)

    def get_element_count(self, selector: str) -> int:
        """
        Получить количество элементов.

        Args:
            selector: CSS селектор

        Returns:
            Количество найденных элементов
        """
        return self.page.locator(selector).count()

    def query_selector_all(self, selector: str, timeout: int = None):
        """
        Найти все элементы по селектору.

        Args:
            selector: CSS селектор
            timeout: Таймаут ожидания

        Returns:
            Список элементов
        """
        if timeout is None:
            timeout = self.DEFAULT_TIMEOUT
        # Ждем появления хотя бы одного элемента
        self.page.wait_for_selector(selector, timeout=timeout)
        return self.page.query_selector_all(selector)
