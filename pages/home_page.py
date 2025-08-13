"""
Главная страница приложения.
Наследует от BasePage для базовой функциональности.
"""
from pages.base_page import BasePage
from playwright.sync_api import Page


class HomePage(BasePage):
    """Класс для работы с главной страницей."""
    
    def __init__(self, page: Page, base_url: str = None):
        super().__init__(page, base_url)
        # Селекторы элементов главной страницы
        self.map_selector = "div#map"
        self.header_selector = "header"
        self.navigation_selector = "nav"
        self.footer_selector = "footer"
    
    def open_homepage(self):
        """Открыть главную страницу."""
        self.open()
        self.wait_for_page_load()
    
    def check_map_visible(self):
        """Проверить видимость карты."""
        self.expect_visible(self.map_selector)
    
    def check_header_visible(self):
        """Проверить видимость заголовка."""
        self.expect_visible(self.header_selector)
    
    def check_navigation_visible(self):
        """Проверить видимость навигации."""
        self.expect_visible(self.navigation_selector)
    
    def check_footer_visible(self):
        """Проверить видимость подвала."""
        self.expect_visible(self.footer_selector)
    
    def check_all_elements(self):
        """Проверить видимость всех основных элементов."""
        self.check_map_visible()
        self.check_header_visible()
        self.check_navigation_visible()
        self.check_footer_visible()
