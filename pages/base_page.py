"""
Базовый класс для Page Object Model (POM).
Простая реализация без избыточности.
"""
from playwright.sync_api import Page, Locator, expect
from typing import Optional


class BasePage:
    """Базовый класс для всех страниц."""
    
    def __init__(self, page: Page, base_url: str = None):
        self.page = page
        self.base_url = base_url or "https://virtualtours.qbd.ae/map"
    
    def open(self, path: str = ""):
        """Открыть страницу."""
        url = f"{self.base_url.rstrip('/')}/{path.lstrip('/')}" if path else self.base_url
        self.page.goto(url)
    
    def wait_for_element(self, selector: str, timeout: int = 10000) -> Locator:
        """Ожидать появления элемента."""
        element = self.page.locator(selector)
        element.wait_for(state="visible", timeout=timeout)
        return element
    
    def click(self, selector: str, timeout: int = 10000):
        """Кликнуть по элементу."""
        element = self.wait_for_element(selector, timeout)
        element.click()
    
    def fill(self, selector: str, text: str, timeout: int = 10000):
        """Заполнить поле."""
        element = self.wait_for_element(selector, timeout)
        element.fill(text)
    
    def get_text(self, selector: str, timeout: int = 10000) -> str:
        """Получить текст элемента."""
        element = self.wait_for_element(selector, timeout)
        return element.text_content()
    
    def is_visible(self, selector: str, timeout: int = 10000) -> bool:
        """Проверить видимость элемента."""
        try:
            self.wait_for_element(selector, timeout)
            return True
        except:
            return False
    
    def expect_visible(self, selector: str, timeout: int = 10000):
        """Ожидать видимости элемента."""
        element = self.wait_for_element(selector, timeout)
        expect(element).to_be_visible()
    
    def wait_for_page_load(self):
        """Ожидать загрузки страницы."""
        self.page.wait_for_load_state("networkidle")
