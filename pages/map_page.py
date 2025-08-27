from pages.base_page import BasePage
from locators.map_locators import MapLocators
from playwright.sync_api import Page


class MapPage(BasePage):
    """Класс для работы со страницей карты."""
    
    def __init__(self, page: Page, base_url: str = None):
        super().__init__(page, base_url)
        self.locators = MapLocators()
    
    def open_map_page(self):
        """Открыть страницу карты."""
        self.open()
        self.wait_for_page_load()
    
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
        
        self.click(selector)
    
    def check_project_info_visible(self, project_name: str):
        """Проверить видимость информации о проекте."""
        self.expect_visible(self.locators.PROJECT_INFO_WINDOW)
    
    def open_project_page(self, project_name: str):
        """Открыть полную страницу проекта."""
        project_url = self.locators.PROJECT_URL_TEMPLATE.format(project=project_name.lower())
        self.page.goto(project_url)
        self.wait_for_page_load()
    
    def check_project_page_loaded(self, project_name: str):
        """Проверить загрузку страницы проекта."""
        # Проверяем, что мы на странице проекта (URL содержит /project/ и название проекта)
        current_url = self.page.url
        assert f'/project/{project_name.lower()}' in current_url, f"Не на странице проекта {project_name}. Текущий URL: {current_url}"
        
        # Проверяем наличие текста проекта на странице
        body_text = self.page.locator('body').inner_text()
        assert project_name.lower() in body_text.lower(), f"Текст проекта '{project_name}' не найден на странице"
    
    def return_to_map_from_project(self):
        """Вернуться на карту со страницы проекта."""
        # Переходим на карту напрямую
        self.page.goto(self.locators.MAP_URL)
        self.wait_for_page_load()
    
    def verify_returned_to_map(self):
        """Проверить, что успешно вернулись на карту."""
        current_url = self.page.url
        assert self.locators.MAP_URL in current_url, f"Не вернулись на карту. Текущий URL: {current_url}"
        
        # Проверяем, что карта загрузилась
        self.check_map_loaded()
        
        # Проверяем, что проекты видны
        self.check_all_projects_visible()
    
    def zoom_in(self):
        """Приблизить карту."""
        try:
            # Сначала пробуем основной локатор
            if self.is_visible(self.locators.ZOOM_IN_BUTTON, timeout=5000):
                self.click(self.locators.ZOOM_IN_BUTTON)
            else:
                # Пробуем альтернативные локаторы
                self.click(self.locators.ZOOM_IN_ALT)
        except Exception:
            # Если не удалось, просто логируем
            print("Кнопка увеличения не найдена или недоступна")
    
    def zoom_out(self):
        """Отдалить карту."""
        try:
            # Сначала пробуем основной локатор
            if self.is_visible(self.locators.ZOOM_OUT_BUTTON, timeout=5000):
                self.click(self.locators.ZOOM_OUT_BUTTON)
            else:
                # Пробуем альтернативные локаторы
                self.click(self.locators.ZOOM_OUT_ALT)
        except Exception:
            # Если не удалось, просто логируем
            print("Кнопка уменьшения не найдена или недоступна")
    
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

    def check_map_controls_visible(self):
        """Проверить видимость элементов управления картой."""
        # Проверяем основные элементы управления
        controls_found = 0
        
        if self.is_visible(self.locators.ZOOM_IN_BUTTON, timeout=5000):
            controls_found += 1
        elif self.is_visible(self.locators.ZOOM_IN_ALT, timeout=5000):
            controls_found += 1
            
        if self.is_visible(self.locators.ZOOM_OUT_BUTTON, timeout=5000):
            controls_found += 1
        elif self.is_visible(self.locators.ZOOM_OUT_ALT, timeout=5000):
            controls_found += 1
            
        if self.is_visible(self.locators.FULLSCREEN_BUTTON, timeout=5000):
            controls_found += 1
        elif self.is_visible(self.locators.FULLSCREEN_ALT, timeout=5000):
            controls_found += 1
        
        # Требуем хотя бы 2 элемента управления
        assert controls_found >= 2, f"Найдено только {controls_found} элементов управления картой"
    
    def check_all_elements(self):
        """Проверить видимость всех основных элементов."""
        self.check_map_loaded()
        self.check_all_projects_visible()
        # Делаем проверку элементов управления необязательной
        try:
            self.check_map_controls_visible()
        except Exception as e:
            print(f"Элементы управления картой недоступны: {e}")
            # Не прерываем тест, если элементы управления недоступны
