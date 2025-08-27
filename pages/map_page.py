from pages.base_page import BasePage
from locators.map_locators import MapLocators
from playwright.sync_api import Page
import os


class MapPage(BasePage):
    """Класс для работы со страницей карты."""
    
    def __init__(self, page: Page, base_url: str = None):
        super().__init__(page, base_url)
        self.locators = MapLocators()
        
        # Динамически определяем URL в зависимости от окружения
        if base_url and ("qube-dev" in base_url or "dev" in base_url):
            self.project_url_template = base_url.replace("/map", "/project/{project}/area")
            self.map_url = base_url
        else:
            # Production URLs из переменных окружения
            prod_base = os.getenv("PROD_BASE_URL", "https://virtualtours.qbd.ae/map")
            self.project_url_template = prod_base.replace("/map", "/project/{project}/area")
            self.map_url = prod_base
    
    def open_map_page(self):
        """Открыть страницу карты."""
        self.open()
        self.wait_for_page_load()
        
        # Убеждаемся, что окно имеет правильный размер
        self.ensure_proper_window_size()
        
        # Дополнительное ожидание загрузки карты и проектов
        self.wait_for_map_and_projects_loaded()
    
    def ensure_proper_window_size(self):
        """Обеспечиваем правильный размер окна для лучшей видимости карты."""
        try:
            # Проверяем текущий размер viewport
            current_size = self.page.viewport_size
            if current_size and (current_size['width'] < 1920 or current_size['height'] < 1080):
                # Устанавливаем Full HD размер
                self.page.set_viewport_size({"width": 1920, "height": 1080})
        except Exception as e:
            print(e)
    
    def wait_for_map_and_projects_loaded(self):
        """Ожидать полной загрузки карты и проектов."""
        try:
            # Сначала ждем загрузки контейнера карты
            self.wait_for_element(self.locators.MAP_CONTAINER, timeout=30000)
            
            # Затем ждем появления хотя бы одного проекта
            # Используем более надежный локатор для ожидания проектов
            self.page.wait_for_selector(
                'div[aria-label*="Elire"], div[aria-label*="ELIRE"], div[aria-label*="Arisha"], div[aria-label*="ARISHA"], div[aria-label*="Cubix"], div[aria-label*="CUBIX"]',
                state="visible",
                timeout=30000
            )
            
            # Дополнительная пауза для стабилизации карты
            self.page.wait_for_timeout(2000)
            
        except Exception as e:
            print(f"Ошибка при ожидании загрузки карты: {e}")
            # Продолжаем выполнение, возможно карта уже загружена

    
    def check_map_loaded(self):
        """Проверить загрузку карты."""
        self.expect_visible(self.locators.MAP_CONTAINER)
    
    def check_all_projects_visible(self):
        """Проверить видимость всех проектов."""
        projects = self.page.locator(self.locators.ALL_PROJECTS).all()
        assert len(projects) == 3, f"Ожидалось 3 проекта, найдено {len(projects)}"
    
    def click_project(self, project_name: str):
        """Кликнуть по проекту на карте."""
        if project_name.lower() == "elire":
            selector = self.locators.PROJECT_ELIRE
        elif project_name.lower() == "arisha":
            selector = self.locators.PROJECT_ARISHA
        elif project_name.lower() == "cubix":
            selector = self.locators.PROJECT_CUBIX
        else:
            raise ValueError(f"Неизвестный проект: {project_name}")
        
        # Дополнительная проверка, что проект действительно видим
        try:
            # Ждем появления конкретного проекта
            self.page.wait_for_selector(
                selector,
                state="visible",
                timeout=30000
            )
            
            # Дополнительная пауза для стабилизации
            self.page.wait_for_timeout(1000)
            
        except Exception as e:
            print(f"Проект {project_name} не найден: {e}")
            # Продолжаем выполнение, возможно элемент уже готов
        
        self.click(selector)
    
    def check_project_info_visible(self, project_name: str):
        """Проверить видимость информации о проекте."""
        self.expect_visible(self.locators.PROJECT_INFO_WINDOW)
    
    def open_project_page(self, project_name: str):
        """Открыть страницу проекта."""
        project_url = self.project_url_template.format(project=project_name.lower())
        self.page.goto(project_url)
        self.wait_for_page_load()
    
    def check_project_page_loaded(self, project_name: str):
        """Проверить загрузку страницы проекта."""
        # Проверяем, что мы на странице проекта (URL содержит /project/ и название проекта)
        self.wait_for_page_load()
        current_url = self.page.url
        self.wait_for_page_load()
        assert f'/project/{project_name.lower()}' in current_url, f"Не на странице проекта {project_name}. Текущий URL: {current_url}"
    
    def return_to_map_from_project(self):
        """Вернуться на карту со страницы проекта."""
        self.page.goto(self.map_url)
        self.wait_for_page_load()
    
    def verify_returned_to_map(self):
        """Проверить, что вернулись на карту."""
        current_url = self.page.url
        assert self.map_url in current_url, f"Не вернулись на карту. Текущий URL: {current_url}"

    
    def toggle_fullscreen(self):
        """Переключить полноэкранный режим."""
        try:
            # Сначала пробуем основной локатор
            if self.is_visible(self.locators.FULLSCREEN_BUTTON, timeout=5000):
                self.click(self.locators.FULLSCREEN_BUTTON)
            else:
                # Пробуем альтернативные локаторы
                self.click(self.locators.FULLSCREEN_ALT)
        except Exception:
            # Если не удалось, просто логируем
            print("Кнопка полноэкранного режима не найдена или недоступна")

    
    def check_all_elements(self):
        """Проверить видимость всех основных элементов."""
        self.check_map_loaded()
        self.check_all_projects_visible()
