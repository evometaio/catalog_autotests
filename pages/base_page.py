import allure
from playwright.sync_api import Page, expect, Locator
from utils.logger import get_logger


class BasePage:
    def __init__(self, page: Page):
        self.page = page
        self.logger = get_logger(f"{self.__class__.__name__}")

    def open(self):
        """Открыть страницу self.URL."""
        with allure.step(f"Открываем {self.URL}"):
            self.logger.info(f"Открываем страницу: {self.URL}")
            self.page.goto(self.URL)
            self.logger.info(f"Страница {self.URL} успешно загружена")

    def wait_for_element(self, selector: str, timeout: int = 10) -> Locator:
        """Ожидает появления элемента на странице."""
        self.logger.info(f"Ожидаем элемент: {selector}")
        locator = self.page.locator(selector)
        locator.wait_for(state="visible", timeout=timeout * 1000)
        return locator

    def click_element(self, selector: str, timeout: int = 10):
        """Кликает по элементу с ожиданием."""
        with allure.step(f"Кликаем по элементу: {selector}"):
            element = self.wait_for_element(selector, timeout)
            element.click()
            self.logger.info(f"Кликнули по элементу: {selector}")

    def fill_input(self, selector: str, text: str, timeout: int = 10):
        """Заполняет поле ввода."""
        with allure.step(f"Заполняем поле {selector} текстом: {text}"):
            element = self.wait_for_element(selector, timeout)
            element.fill(text)
            self.logger.info(f"Заполнили поле {selector} текстом: {text}")

    def get_text(self, selector: str, timeout: int = 10) -> str:
        """Получает текст элемента."""
        element = self.wait_for_element(selector, timeout)
        text = element.text_content()
        self.logger.info(f"Получили текст элемента {selector}: {text}")
        return text

    def is_element_visible(self, selector: str, timeout: int = 10) -> bool:
        """Проверяет видимость элемента."""
        try:
            self.wait_for_element(selector, timeout)
            return True
        except:
            return False

    def take_screenshot(self, name: str = None) -> bytes:
        """Делает скриншот страницы."""
        import time
        name = name or f"screenshot_{int(time.time())}"
        screenshot = self.page.screenshot()
        
        with allure.step(f"Делаем скриншот: {name}"):
            allure.attach(screenshot, name=name, attachment_type=allure.attachment_type.PNG)
            self.logger.info(f"Сделан скриншот: {name}")
        
        return screenshot

    def get_page_title(self) -> str:
        """Получает заголовок страницы."""
        title = self.page.title()
        self.logger.info(f"Заголовок страницы: {title}")
        return title
