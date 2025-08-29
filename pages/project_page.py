import os
import time

from locators.map_locators import MapLocators
from locators.project_locators import ProjectLocators
from playwright.sync_api import Page
from pages.map_page import MapPage

class ProjectPage(MapPage):
    """
    Класс для работы со страницей проекта (агенсткий роут)
    """
    def __init__(self, page: Page, base_url: str = None):
        super().__init__(page, base_url)
        self.map_locators = MapLocators()
        self.project_locators = ProjectLocators()

    def open_agent_page(self):
        """Открыть страницу проекта (агент роут)."""
        self.open()
        self.wait_for_page_load()

    def click_on_agent_project(self, project_name: str):
        """Кликнуть на проект и затем на кнопку Explore Project."""
        self.wait_for_map_and_projects_loaded()
        # Сначала кликаем на проект (используем метод из MapPage)
        self.click_project(project_name)
        self.expect_visible(self.map_locators.PROJECT_INFO_WINDOW)
        self.expect_visible(self.map_locators.EXPLORE_PROJECT_BUTTON)
        # Затем кликаем на кнопку Explore Project
        self.click(self.map_locators.EXPLORE_PROJECT_BUTTON)
        self.wait_for_page_load()


    def click_on_all_units_button(self, project_name: str = "arisha"):
        """Кликнуть на кнопку All units."""
        self.expect_visible(self.project_locators.ALL_UNITS_BUTTON)
        self.click(self.project_locators.ALL_UNITS_BUTTON)

    def click_on_avialable_apartment(self):
        """Кликнуть на квартиру, которая доступна для просмотра."""
        self.expect_visible(self.project_locators.AVIALABLE_APART_CARD)
        self.click(self.project_locators.AVIALABLE_APART_CARD)
        apart_text = self.get_text(self.project_locators.AVIALABLE_APART)
        assert apart_text == "APARTMENT 104"

    def click_on_sales_offer_button(self):
        """Кликнуть на кнопку Sales Offer."""
        self.expect_visible(self.project_locators.SALES_OFFER_BUTTON)
        self.click(self.project_locators.SALES_OFFER_BUTTON)

    def download_pdf_and_verify(self) -> tuple[bool, str]:
        """
        Скачать PDF в директорию и проверить что файл не пустой.

        Returns:
            tuple: (успех, путь к файлу)
        """
        try:
            # Создаем директорию для скачиваний
            download_dir = "temp/downloads"
            os.makedirs(download_dir, exist_ok=True)

            # Начинаем скачивание
            with self.page.expect_download() as download_info:
                # Кликаем по кнопке Download PDF
                self.expect_visible(self.project_locators.DOWNLOAD_PDF_BUTTON)
                self.click(self.project_locators.DOWNLOAD_PDF_BUTTON)

            # Получаем объект скачивания
            download = download_info.value

            # Проверяем что файл скачался
            if not download or not download.suggested_filename:
                return False, ""

            # Проверяем что это PDF
            if not download.suggested_filename.lower().endswith('.pdf'):
                return False, ""

            # Сохраняем файл в нашу директорию
            file_path = os.path.join(download_dir, download.suggested_filename)
            download.save_as(file_path)

            # Проверяем размер файла (больше 1KB)
            file_size = os.path.getsize(file_path)

            print(f"PDF скачан: {file_path}, размер: {file_size} байт")
            return file_size > 1024, file_path

        except Exception as e:
            return False, ""

    def cleanup_after_test(self):
        """Очистка через системную команду."""
        os.system("rm -rf temp")