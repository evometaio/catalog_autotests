from pages.base_page import BasePage
from locators.map_locators import MapLocators
from playwright.sync_api import Page

class ProjectPage(BasePage):
    """
    Класс для работы со страницей проекта
    """
    def __init__(self, page: Page, base_url: str = None):
        super().__init__(page, base_url)
        self.locators = MapLocators()