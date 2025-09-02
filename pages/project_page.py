import os

from playwright.sync_api import Page

from locators.map_locators import MapLocators
from locators.project_locators import QubePageLocators
from pages.map_page import MapPage


class ProjectPage(MapPage):
    """
    Класс для работы со страницей проекта (агенсткий роут)
    """

    def __init__(self, page: Page, base_url: str = None):
        super().__init__(page, base_url)
        self.map_locators = MapLocators()
        self.project_locators = QubePageLocators()

    def open_agent_page(self):
        """Открыть страницу проекта (агент роут)."""
        self.open()

    def open_client_page(self):
        """Открыть страницу проекта (клиент роут)."""
        self.open()

    def fill_in_the_callback_form_on_project_client_page(self):
        """Заполнить поля формы Callback."""
        self.expect_visible(self.project_locators.ClientPage.CALLBACK_FORM_BUTTON)
        self.click(self.project_locators.ClientPage.CALLBACK_FORM_BUTTON)

    def click_on_project(self, project_name: str):
        """Кликнуть на проект и затем на кнопку Explore Project."""
        self.wait_for_map_and_projects_loaded()
        # Сначала кликаем на проект (используем метод из MapPage)
        self.click_project(project_name)
        self.expect_visible(self.map_locators.PROJECT_INFO_WINDOW)
        self.expect_visible(self.map_locators.EXPLORE_PROJECT_BUTTON)
        # Затем кликаем на кнопку Explore Project
        self.click(self.map_locators.EXPLORE_PROJECT_BUTTON)
        self.wait_for_page_load()

    def click_on_all_units_button(self):
        """Кликнуть на кнопку All units."""
        self.expect_visible(self.project_locators.ALL_UNITS_BUTTON)
        self.click(self.project_locators.ALL_UNITS_BUTTON)

    def click_on_residences_button_and_request_viewing_form(self):
        """Кликнуть на кнопку Residences."""
        self.expect_visible(self.project_locators.Elire.RESIDENCES_BUTTON)
        self.click(self.project_locators.Elire.RESIDENCES_BUTTON)
        self.click(self.project_locators.Elire.REQUEST_VIEWING_BUTTON)

    def find_and_click_available_apartment(self):
        """
        Найти и кликнуть на первый доступный апартамент (без замка).
        
        Returns:
            str: Название выбранного апартамента
        """
        # Небольшая пауза для загрузки страницы
        self.page.wait_for_timeout(2000)
        
        # Получаем все заголовки апартаментов
        apartment_titles = self.page.locator(self.project_locators.ALL_APARTMENT_TITLES)
        apartment_count = apartment_titles.count()
        
        if apartment_count == 0:
            raise Exception("Апартаменты не найдены на странице")
        
        print(f"Найдено {apartment_count} апартаментов")
        
        # Ищем первый доступный апартамент (без замка)
        for i in range(apartment_count):
            apartment_title = apartment_titles.nth(i)
            apartment_text = apartment_title.text_content()
            
            # Проверяем, есть ли замок у этого апартамента
            # Ищем замок внутри заголовка апартамента
            lock_icon = apartment_title.locator("xpath=.//span[@role='img' and @aria-label='lock']")
            has_lock = lock_icon.count() > 0
            
            print(f"Апартамент {apartment_text}: {'заблокирован' if has_lock else 'доступен'}")
            
            # Если замка нет, кликаем по этому апартаменту
            if not has_lock:
                print(f"Выбираем доступный апартамент: {apartment_text}")
                # Используем JavaScript клик для надежности
                apartment_title.evaluate("element => element.click()")
                return apartment_text
        
        # Если все апартаменты заблокированы
        raise Exception("Все апартаменты заблокированы (имеют замок)")

    def click_on_avialable_apart_on_cubix(self):
        self.expect_visible(self.project_locators.Cubix.AVIALABLE_APART_CARD)
        self.click(self.project_locators.Cubix.AVIALABLE_APART_CARD)

    def click_on_sales_offer_button(self):
        """Кликнуть на кнопку Sales Offer."""
        self.expect_visible(self.project_locators.AgentPage.SALES_OFFER_BUTTON)
        self.click(self.project_locators.AgentPage.SALES_OFFER_BUTTON)

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

    def mock_request_viewing_api(self, project_name: str = None, configuration: str = None):
        """
        Настраивает мок для API запроса формы Request Viewing.
        
        Args:
            project_name: Название проекта (elire, arisha, cubix)
            configuration: Конфигурация (1br-residence, 2br-residence, etc.)
        """
        def handle_route(route):
            # Генерируем уникальный ID для мок-запроса
            import time
            mock_id = f"mock_{int(time.time())}"
            
            route.fulfill(
                status=200,
                content_type="text/x-component",
                body=f'0:["$@1",["{mock_id}",null]]\n1:{{"success":true,"error":null,"status":201}}'
            )
        
        # Если указаны конкретные параметры, мокаем только их
        if project_name and configuration:
            route_pattern = f"**/client/project/{project_name}/configuration/{configuration}"
        else:
            # Универсальный паттерн для всех проектов
            route_pattern = "**/client/project/*/configuration/*"
        
        self.page.route(route_pattern, handle_route)
        print(f"🔒 API мок настроен для: {route_pattern}")

    def send_request_viewing_form(self, fake):
        """
        Заполняет и отправляет форму Request Viewing с данными из Faker.
        
        Args:
            fake: Экземпляр Faker для генерации данных
        """
        # Генерируем данные с помощью Faker
        form_data = {
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "phone": fake.phone_number(),
            "email": fake.email(),
            "note": fake.text(max_nb_chars=100)
        }
        
        # Заполняем поля формы
        if "first_name" in form_data:
            self.fill("(//input[@id='first_name'])[1]", form_data["first_name"])
        if "last_name" in form_data:
            self.fill("(//input[@id='last_name'])[1]", form_data["last_name"])
        if "phone" in form_data:
            self.fill("(//input[@id='phone'])[1]", form_data["phone"])
        if "email" in form_data:
            self.fill("(//input[@id='email'])[1]", form_data["email"])
        if "note" in form_data:
            self.fill("(//textarea[@id='note'])[1]", form_data["note"])
        
        # Кликаем на кнопку отправки
        self.click(self.project_locators.Elire.SUBMIT_BUTTON_FOR_REQUEST_VIEWING)


    def is_success_message_displayed(self) -> bool:
        """
        Проверяет, отображается ли сообщение об успешной отправке.
        
        Returns:
            bool: True если сообщение об успехе отображается
        """
        try:
            # Ждем появления сообщения об успехе
            success_selectors = [
                'text="Thank you!"',
                'text="Our specialist will contact you shortly."',
                'text="Thank you! Our specialist will contact you shortly."',
                'text="Request submitted successfully"',
                'text="Thank you for your request"',
                'text="Your request has been sent"',
                '[class*="success"]',
                '[class*="message"]'
            ]
            
            for selector in success_selectors:
                if self.page.locator(selector).count() > 0:
                    return True
            
            return False
        except Exception as e:
            return False
