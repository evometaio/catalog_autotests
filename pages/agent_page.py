"""Page Object для агентских страниц всех проектов."""

import os
import time

from .base_page import BasePage
from locators.project_locators import QubePageLocators
from locators.map_locators import MapLocators


class AgentPage(BasePage):
    """Page Object для агентских страниц."""

    def __init__(self, page, url: str):
        """Инициализация AgentPage.
        
        Args:
            page: Playwright page объект
            url: URL агентской страницы
        """
        super().__init__(page, url)
        self.project_locators = QubePageLocators()
        self.map_locators = MapLocators()



    def click_on_download_pdf_button(self):
        """Кликает на кнопку скачивания PDF."""
        self.click(self.locators.DOWNLOAD_PDF_BUTTON)

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
                self.expect_visible(self.project_locators.AgentPage.DOWNLOAD_PDF_BUTTON)
                self.click(self.project_locators.AgentPage.DOWNLOAD_PDF_BUTTON)

            # Получаем объект скачивания
            download = download_info.value

            # Проверяем что файл скачался
            if not download or not download.suggested_filename:
                return False, ""

            # Проверяем что это PDF
            if not download.suggested_filename.lower().endswith(".pdf"):
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

    def cleanup_pdf_after_test(self):
        """Очистка через системную команду."""
        os.system("rm -rf temp")

    def click_on_project(self, project_name: str):
        """Кликнуть на проект и затем на кнопку Explore Project."""
        self.wait_for_map_and_projects_loaded()
        # Сначала кликаем на проект (используем метод из BasePage)
        self.click_project(project_name)
        self.expect_visible(self.map_locators.PROJECT_INFO_WINDOW)
        self.expect_visible(self.map_locators.EXPLORE_PROJECT_BUTTON)
        
        # Затем кликаем на кнопку Explore Project
        self.click(self.map_locators.EXPLORE_PROJECT_BUTTON)

        # Ждем изменения URL
        self.page.wait_for_url("**/area", timeout=10000)
        self.wait_for_page_load()

    def click_on_all_units_button(self):
        """Кликнуть на кнопку All units."""
        self.expect_visible(self.project_locators.ALL_UNITS_BUTTON)
        self.click(self.project_locators.ALL_UNITS_BUTTON)
        
        # Ждем изменения URL на catalog_2d
        self.page.wait_for_url("**/catalog_2d", timeout=10000)


    def find_and_click_available_apartment(self, project_name: str = None):
        """
        Найти и кликнуть на первый доступный апартамент (без замка).
        Универсальный метод для всех проектов.

        Args:
            project_name: Название проекта (используется только для логирования)

        Returns:
            str: Название выбранного апартамента
        """
        # Ждем загрузки апартаментов
        self.page.wait_for_selector(self.project_locators.ALL_APARTMENT_TITLES, state="attached", timeout=10000)
        
        # Используем локатор из project_locators.py
        apartment_titles = self.page.locator(self.project_locators.ALL_APARTMENT_TITLES)
        apartment_count = apartment_titles.count()

        if apartment_count == 0:
            raise Exception("Апартаменты не найдены на странице")

        # Ищем первый доступный апартамент (без замка)
        for i in range(apartment_count):
            apartment_title = apartment_titles.nth(i)
            apartment_text = apartment_title.text_content()

            # Проверяем, есть ли замок у этого апартамента
            lock_icon = apartment_title.locator(
                "xpath=.//span[@role='img' and @aria-label='lock']"
            )
            has_lock = lock_icon.count() > 0

            # Если замка нет, кликаем по этому апартаменту
            if not has_lock:
                apartment_title.evaluate("element => element.click()")
                return apartment_text

        # Если все апартаменты заблокированы
        raise Exception("Все апартаменты заблокированы (имеют замок)")

    def click_on_sales_offer_button(self):
        """Кликнуть на кнопку Sales Offer."""
        self.expect_visible(self.project_locators.AgentPage.SALES_OFFER_BUTTON)
        self.click(self.project_locators.AgentPage.SALES_OFFER_BUTTON)

