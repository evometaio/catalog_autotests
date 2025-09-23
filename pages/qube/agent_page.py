import os
import time

from locators.map_locators import MapLocators
from locators.project_locators import QubePageLocators

from ..base_page import BasePage


class AgentPage(BasePage):
    """Page Object для агентских страниц Qube проектов."""

    def __init__(self, page, url: str):
        """Инициализация AgentPage.

        Args:
            page: Playwright page объект
            url: URL агентской страницы
        """
        super().__init__(page, url, QubePageLocators)

    def click_on_download_pdf_button(self):
        """Кликает на кнопку скачивания PDF."""
        self.click(self.project_locators.DOWNLOAD_PDF_BUTTON)

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

            # Засекаем время начала скачивания
            start_time = time.time()

            # Начинаем скачивание с таймаутом 20 секунд
            with self.page.expect_download(timeout=20000) as download_info:
                # Кликаем по кнопке Download PDF
                self.expect_visible(self.project_locators.DOWNLOAD_PDF_BUTTON)
                self.click(self.project_locators.DOWNLOAD_PDF_BUTTON)

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

            # Засекаем время окончания скачивания
            end_time = time.time()
            download_time = round(end_time - start_time, 2)

            # Проверяем размер файла (больше 1KB)
            file_size = os.path.getsize(file_path)

            print(
                f"PDF скачан: {file_path}, размер: {file_size} байт, время скачивания: {download_time} сек"
            )
            return file_size > 1024, file_path

        except Exception as e:
            print(f"Ошибка при скачивании PDF: {e}")
            return False, ""

    def cleanup_pdf_after_test(self):
        """Очистка через системную команду."""
        os.system("rm -rf temp")

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
        self.page.wait_for_selector(
            self.project_locators.ALL_APARTMENT_TITLES, state="attached", timeout=10000
        )

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
        self.expect_visible(self.project_locators.SALES_OFFER_BUTTON)
        self.click(self.project_locators.SALES_OFFER_BUTTON)
