"""Кастомные assertions с понятными сообщениями об ошибках."""

from playwright.sync_api import Page


class Assertions:
    """
    Класс для проверок с кастомными сообщениями об ошибках.
    
    Ответственность:
    - Проверки с понятными сообщениями
    - Унифицированный формат ошибок
    """

    def __init__(self, page: Page):
        """
        Инициализация.
        
        Args:
            page: Playwright Page объект
        """
        self.page = page

    def assert_that(self, condition: bool, error_message: str):
        """
        Базовый assertion.
        
        Args:
            condition: Условие которое должно быть True
            error_message: Сообщение об ошибке если условие False
        """
        assert condition, f"❌ {error_message}"

    def assert_element_visible(
        self, 
        selector: str, 
        error_message: str, 
        timeout: int = 10000
    ):
        """
        Проверить что элемент видим.
        
        Args:
            selector: CSS селектор элемента
            error_message: Сообщение об ошибке
            timeout: Таймаут ожидания
        """
        try:
            element = self.page.locator(selector)
            element.wait_for(state="visible", timeout=timeout)
            is_visible = element.is_visible()
        except:
            is_visible = False
            
        assert is_visible, f"❌ {error_message}\n   Селектор: {selector}"

    def assert_element_not_visible(
        self, 
        selector: str, 
        error_message: str, 
        timeout: int = 2000
    ):
        """
        Проверить что элемент НЕ видим.
        
        Args:
            selector: CSS селектор элемента
            error_message: Сообщение об ошибке
            timeout: Таймаут проверки
        """
        try:
            element = self.page.locator(selector)
            element.wait_for(state="visible", timeout=timeout)
            is_visible = element.is_visible()
        except:
            is_visible = False
            
        assert not is_visible, f"❌ {error_message}\n   Селектор: {selector}"

    def assert_url_contains(self, expected_substring: str, error_message: str):
        """
        Проверить что URL содержит подстроку.
        
        Args:
            expected_substring: Ожидаемая подстрока в URL
            error_message: Сообщение об ошибке
        """
        current_url = self.page.url
        assert expected_substring in current_url, (
            f"❌ {error_message}\n"
            f"   Ожидаемая подстрока: '{expected_substring}'\n"
            f"   Текущий URL: {current_url}"
        )

    def assert_url_equals(self, expected_url: str, error_message: str):
        """
        Проверить что URL равен ожидаемому.
        
        Args:
            expected_url: Ожидаемый URL
            error_message: Сообщение об ошибке
        """
        current_url = self.page.url
        assert current_url == expected_url, (
            f"❌ {error_message}\n"
            f"   Ожидался URL: {expected_url}\n"
            f"   Текущий URL: {current_url}"
        )

    def assert_text_equals(
        self, 
        selector: str, 
        expected_text: str, 
        error_message: str,
        timeout: int = 10000
    ):
        """
        Проверить что текст элемента равен ожидаемому.
        
        Args:
            selector: CSS селектор элемента
            expected_text: Ожидаемый текст
            error_message: Сообщение об ошибке
            timeout: Таймаут ожидания
        """
        element = self.page.locator(selector)
        element.wait_for(state="visible", timeout=timeout)
        actual_text = element.text_content()
        
        assert actual_text == expected_text, (
            f"❌ {error_message}\n"
            f"   Ожидалось: '{expected_text}'\n"
            f"   Получено: '{actual_text}'"
        )

    def assert_text_contains(
        self,
        selector: str,
        expected_substring: str,
        error_message: str,
        timeout: int = 10000,
    ):
        """
        Проверить что текст элемента содержит подстроку.
        
        Args:
            selector: CSS селектор элемента
            expected_substring: Ожидаемая подстрока
            error_message: Сообщение об ошибке
            timeout: Таймаут ожидания
        """
        element = self.page.locator(selector)
        element.wait_for(state="visible", timeout=timeout)
        actual_text = element.text_content()
        
        assert expected_substring in actual_text, (
            f"❌ {error_message}\n"
            f"   Ожидаемая подстрока: '{expected_substring}'\n"
            f"   Фактический текст: '{actual_text}'"
        )

