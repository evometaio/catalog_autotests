from playwright.sync_api import Locator, Page, expect

from locators.map_locators import MapLocators


class BasePage:
    """Базовый класс для всех страниц."""

    def __init__(self, page: Page, base_url: str = None):
        self.locators = MapLocators()
        self.page = page
        self.base_url = base_url

    def open(self, path: str = ""):
        """Открыть страницу."""
        url = (
            f"{self.base_url.rstrip('/')}/{path.lstrip('/')}" if path else self.base_url
        )
        self.page.goto(url)
        self.wait_for_page_load()

        current_url = self.get_current_url()
        assert (
            url in current_url
        ), f"Не удалось открыть страницу. Ожидалось: {url}, Получено: {current_url}"

    def wait_for_element(self, selector: str, timeout: int = 20000) -> Locator:
        """Ожидать появления элемента."""
        element = self.page.locator(selector)
        element.wait_for(state="visible", timeout=timeout)
        return element

    def get_current_url(self) -> str:
        """Получить текущий URL."""
        return self.page.url

    def wait_for_map_and_projects_loaded(self):
        """Ожидать полной загрузки карты и проектов."""
        try:
            # Сначала ждем загрузки контейнера карты
            self.wait_for_element(self.locators.MAP_CONTAINER, timeout=30000)

            # Затем ждем появления хотя бы одного проекта
            # Используем более надежный локатор для ожидания проектов
            self.page.wait_for_selector(
                'div[aria-label*="Elire"], div[aria-label*="ELIRE"], div[aria-label*="Arisha"], div[aria-label*="ARISHA"], div[aria-label*="Cubix"], div[aria-label*="CUBIX"], div[aria-label*="Peylaa"], div[aria-label*="Peylaa"], div[aria-label*="Tranquil"]',
                state="visible",
                timeout=30000,
            )

            # Дополнительная пауза для стабилизации карты
            self.page.wait_for_timeout(2000)

        except Exception as e:
            print(f"Ошибка при ожидании загрузки карты: {e}")

    def click(self, selector: str, timeout: int = 20000):
        """Кликнуть по элементу."""
        element = self.wait_for_element(selector, timeout)
        expect(element).to_be_enabled()
        expect(element).to_be_visible()
        element.click()

    def fill(self, selector: str, text: str, timeout: int = 20000):
        """Заполнить поле."""
        element = self.wait_for_element(selector, timeout)
        element.fill(text)

    def get_text(self, selector: str, timeout: int = 20000) -> str:
        """Получить текст элемента."""
        element = self.wait_for_element(selector, timeout)
        return element.text_content()

    def is_visible(self, selector: str, timeout: int = 20000) -> bool:
        """Проверить видимость элемента."""
        try:
            self.wait_for_element(selector, timeout)
            return True
        except:
            return False

    def expect_visible(self, selector: str, timeout: int = 20000):
        """Ожидать видимости элемента."""
        element = self.wait_for_element(selector, timeout)
        expect(element).to_be_visible()

    def wait_for_page_load(self):
        """Ожидать загрузки страницы."""
        self.page.wait_for_load_state("networkidle")

    def assert_url_equals(self, expected_url: str, timeout: int = 10000):
        """Проверить, что URL точно равен ожидаемому.

        Args:
            expected_url: Ожидаемый URL
            timeout: Таймаут ожидания изменения URL
        """
        current_url = self.get_current_url()
        assert (
            current_url == expected_url
        ), f"URL не совпадает. Ожидалось: {expected_url}, Получено: {current_url}"
