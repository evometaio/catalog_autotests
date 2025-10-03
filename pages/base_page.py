from playwright.sync_api import Locator, Page, expect

from locators.map_locators import MapLocators
from locators.project_locators import (
    BaseProjectLocators,
    CapstonePageLocators,
    QubeLocators,
    WellcubePageLocators,
)


class BasePage:
    """Базовый класс для всех страниц."""

    # Константы для таймаутов
    DEFAULT_TIMEOUT = 10000
    LONG_TIMEOUT = 15000
    SHORT_TIMEOUT = 5000
    MAP_LOAD_TIMEOUT = 20000

    def __init__(
        self, page: Page, base_url: str = None, project_locators_class: type = None
    ):
        self.locators = MapLocators()
        # Используем переданный класс локаторов или базовый по умолчанию
        if project_locators_class:
            self.project_locators = project_locators_class()
        else:
            self.project_locators = BaseProjectLocators()
        self.page = page
        self.base_url = base_url

        # URL-ы для навигации (если base_url содержит /map)
        if base_url and "/map" in base_url:
            self.project_url_template = base_url.replace(
                "/map", "/project/{project}/area"
            )
            self.map_url = base_url

        # Инициализируем внутренние классы для организации методов
        self.map_navigation = self.MapNavigation(self)
        self.project = self.ProjectPage(self)
        self.amenities = self.Amenities(self)
        self.area_tour_360 = self.AreaTour360(self)
        self.elire = self.Elire(self)
        self.apartment_widget = self.ApartmentWidget(self)
        self.apartment_info = self.ApartmentInfo(self)

    def open(self, path: str = "", route_type: str = None):
        """Открыть страницу.

        Args:
            path: Дополнительный путь к базовому URL
            route_type: Тип роута для проверки - "client", "agent" или "map"
        """
        url = (
            f"{self.base_url.rstrip('/')}/{path.lstrip('/')}" if path else self.base_url
        )
        self.page.goto(url)
        self.wait_for_page_load()

        # Принудительно сбрасываем масштаб страницы
        self.page.evaluate("document.body.style.zoom = '1'")
        self.page.evaluate("document.documentElement.style.zoom = '1'")

        current_url = self.get_current_url()
        assert (
            url in current_url
        ), f"Не удалось открыть страницу. Ожидалось: {url}, Получено: {current_url}"

        # Проверяем тип роута, если указан
        if route_type:
            if route_type == "client":
                assert (
                    "client" in current_url
                ), f"Не открылась клиентская страница. URL: {current_url}"
            elif route_type == "agent":
                assert (
                    "agent" in current_url
                ), f"Не открылась агентская страница. URL: {current_url}"
            elif route_type == "map":
                assert (
                    "map" in current_url
                ), f"Не открылась страница карты. URL: {current_url}"

    def wait_for_element(self, selector: str, timeout: int = None) -> Locator:
        """Ожидать появления элемента."""
        if timeout is None:
            timeout = self.DEFAULT_TIMEOUT
        element = self.page.locator(selector)

        try:
            # Ждем появления элемента
            element.wait_for(state="visible", timeout=timeout)
            return element
        except TimeoutError as e:
            # Преобразуем TimeoutError в AssertionError для FAILED статуса в Allure
            raise AssertionError(f"Элемент '{selector}' не найден за {timeout}ms.")

    def get_current_url(self) -> str:
        """Получить текущий URL."""
        return self.page.url

    def get_project_url(self, project_name: str, page_type: str = "catalog_2d"):
        """Получить URL для конкретного проекта и типа страницы.

        Args:
            project_name: Название проекта (arisha, cubix, elire, peylaa, tranquil)
            page_type: Тип страницы (catalog_2d, area, map)

        Returns:
            str: URL для проекта
        """
        from conftest import _get_urls_by_environment

        urls = _get_urls_by_environment()
        project_name_lower = project_name.lower()

        # Проверяем валидность типа страницы
        if page_type not in self.project_locators.PAGE_TYPES:
            raise ValueError(f"Неизвестный тип страницы: {page_type}")

        # Определяем базовый URL и URL карты в зависимости от проекта
        # Проверяем тип проекта универсально
        from locators.project_locators import (
            CapstonePageLocators,
            QubeLocators,
            WellcubePageLocators,
        )

        if project_name_lower in QubeLocators.QUBE_PROJECTS:
            # Qube проекты
            base_url = urls["map"].replace("/map", "")
            map_url = urls["map"]
        elif project_name_lower in CapstonePageLocators.CAPSTONE_PROJECTS:
            # Capstone проект
            base_url = urls["capstone_map"].replace("/map", "")
            map_url = urls["capstone_map"]
        elif project_name_lower in WellcubePageLocators.WELLCUBE_PROJECTS:
            # Wellcube проект
            base_url = urls["wellcube_map"].replace("/map", "")
            map_url = urls["wellcube_map"]
        else:
            raise ValueError(f"Неизвестный проект: {project_name}")

        # Формируем полный URL
        if page_type == "catalog_2d":
            return f"{base_url}/project/{project_name_lower}/catalog_2d"
        elif page_type == "area":
            return f"{base_url}/project/{project_name_lower}/area"
        elif page_type == "map":
            return map_url

    def click(self, selector: str, timeout: int = None):
        """Кликнуть по элементу."""
        element = self.wait_for_element(selector, timeout)

        # Проверяем, что элемент активен для клика
        assert element.is_enabled(), f"Элемент {selector} неактивен - баг в UI"

        element.click()

    def fill(self, selector: str, text: str, timeout: int = None):
        """Заполнить поле."""
        element = self.wait_for_element(selector, timeout)
        element.fill(text)

    def get_text(self, selector: str, timeout: int = None) -> str:
        """Получить текст элемента."""
        element = self.wait_for_element(selector, timeout)
        return element.text_content()

    def is_visible(self, selector: str, timeout: int = None) -> bool:
        """Проверить видимость элемента."""
        try:
            self.wait_for_element(selector, timeout)
            return True
        except:
            return False

    def expect_visible(self, selector: str, timeout: int = None):
        """Ожидать видимости элемента."""
        element = self.wait_for_element(selector, timeout)
        assert element.is_visible(), f"Элемент {selector} не отображается - баг в UI"

    def wait_for_page_load(self):
        """Ожидать загрузки страницы."""
        self.page.wait_for_load_state("domcontentloaded")

    def assert_url_equals(self, expected_url: str):
        """Проверить, что URL точно равен ожидаемому.

        Args:
            expected_url: Ожидаемый URL
        """
        current_url = self.get_current_url()
        assert (
            current_url == expected_url
        ), f"URL не совпадает. Ожидалось: {expected_url}, Получено: {current_url}"

    # Методы для работы с картой (перенесены в MapNavigation класс)

    def _get_project_selector(self, project_name: str) -> str:
        """Получить селектор для проекта по названию."""
        import os

        project_name_lower = project_name.lower()
        device = os.getenv("MOBILE_DEVICE", "desktop")

        # Проверяем, запущен ли тест на мобильном устройстве
        if device != "desktop":
            # Для мобильных устройств используем aria-label локаторы
            # На основе отладки: aria-label="ARISHA TERACCES"
            if project_name_lower == "arisha":
                return 'div[aria-label="ARISHA TERACCES"]'
            elif project_name_lower == "elire":
                return 'div[aria-label="ELIRE"]'
            elif project_name_lower == "cubix":
                return 'div[aria-label="CUBIX RESIDENCE"]'
            else:
                # Fallback для других проектов
                return f'div[aria-label*="{project_name.upper()}"]'

        # Получаем проект из локаторов
        project_class = self._get_project_class(project_name_lower)
        if not project_class:
            # Fallback на старый способ
            return f'div[aria-label*="{project_name}"], div[aria-label*="{project_name.upper()}"]'

        # Для Peylaa учитываем окружение
        if project_name_lower == "peylaa":
            environment = os.getenv("TEST_ENVIRONMENT", "dev")
            if environment == "dev":
                return project_class.MAP_LOCATOR_DEV
            else:
                return project_class.MAP_LOCATOR_PROD

        # Для остальных проектов используем MAP_LOCATOR
        return project_class.MAP_LOCATOR

    def _get_project_class(self, project_name: str):
        """Получить класс проекта из локаторов."""
        # Проверяем все проекты в локаторах
        if hasattr(self.project_locators, "ALL_PROJECTS"):
            for project_class in self.project_locators.ALL_PROJECTS:
                if (
                    hasattr(project_class, "PROJECT_NAME")
                    and project_class.PROJECT_NAME == project_name
                ):
                    return project_class
        return None

    # Методы для работы с Explore Amenities (перенесены в Amenities класс)

    # Методы из ProjectPage для работы с проектами

    def click_on_all_units_button(self):
        """Кликнуть на кнопку All units."""
        self.click(self.project_locators.ALL_UNITS_BUTTON)

    def click_on_sales_offer_button(self):
        """Кликнуть на кнопку Sales Offer."""
        self.click(self.project_locators.SALES_OFFER_BUTTON)

    # Методы для работы с 360 Area Tour (перенесены в AreaTour360 класс)

    # Методы для инкапсуляции работы с page
    def click_element(self, selector: str, timeout: int = None):
        """Кликнуть по элементу по селектору."""
        if timeout is None:
            timeout = self.DEFAULT_TIMEOUT
        element = self.page.locator(selector)
        element.wait_for(state="visible", timeout=timeout)
        element.click()

    def query_selector_all(self, selector: str, timeout: int = None):
        """Найти все элементы по селектору."""
        if timeout is None:
            timeout = self.DEFAULT_TIMEOUT
        # Ждем появления хотя бы одного элемента
        self.page.wait_for_selector(selector, timeout=timeout)
        return self.page.query_selector_all(selector)

    def wait_for_timeout(self, timeout: int):
        """Ждать указанное количество миллисекунд."""
        self.page.wait_for_timeout(timeout)

    def is_element_visible(self, selector: str, timeout: int = None) -> bool:
        """Проверить, виден ли элемент."""
        if timeout is None:
            timeout = self.DEFAULT_TIMEOUT
        try:
            element = self.page.locator(selector)
            element.wait_for(state="visible", timeout=timeout)
            return True
        except:
            return False

    def get_element_text(self, selector: str, timeout: int = None) -> str:
        """Получить текст элемента."""
        if timeout is None:
            timeout = self.DEFAULT_TIMEOUT
        element = self.page.locator(selector)
        element.wait_for(state="visible", timeout=timeout)
        return element.text_content()

    def get_element_count(self, selector: str, timeout: int = None) -> int:
        """Получить количество элементов по селектору."""
        if timeout is None:
            timeout = self.DEFAULT_TIMEOUT
        # Ждем появления хотя бы одного элемента
        self.page.wait_for_selector(selector, timeout=timeout)
        return self.page.locator(selector).count()

    # ==================== МЕТОДЫ-ОБЕРТКИ ДЛЯ ОБРАТНОЙ СОВМЕСТИМОСТИ ====================

    # Методы для работы с картой (делегируются к map_navigation)
    def wait_for_map_and_projects_loaded(self):
        """Ожидать полной загрузки карты и проектов."""
        return self.map_navigation.wait_for_map_and_projects_loaded()

    def check_map_loaded(self):
        """Проверить загрузку карты."""
        return self.map_navigation.check_map_loaded()

    def click_project(self, project_name: str):
        """Кликнуть по проекту на карте по названию."""
        return self.map_navigation.click_project(project_name)

    def click_project_on_map(self, project_name: str):
        """Кликнуть на проект и затем на кнопку Explore Project."""
        return self.map_navigation.click_project_on_map(project_name)

    def check_project_info_visible(self, project_name: str):
        """Проверить видимость информации о проекте."""
        return self.map_navigation.check_project_info_visible(project_name)

    def check_project_page_loaded(self, project_name: str):
        """Проверить загрузку страницы проекта."""
        return self.map_navigation.check_project_page_loaded(project_name)

    def return_to_map_from_project_and_verify_returned_to_map(self):
        """Вернуться на карту со страницы проекта."""
        return (
            self.map_navigation.return_to_map_from_project_and_verify_returned_to_map()
        )

    # Методы для работы с amenities (делегируются к amenities)
    def click_explore_amenities_button(self):
        """Кликнуть на кнопку Explore Amenities."""
        return self.amenities.click_explore_amenities_button()

    def verify_amenities_modal_displayed(self):
        """Проверить отображение модального окна amenities."""
        return self.amenities.verify_amenities_modal_displayed()

    def verify_amenities_modal_title(self):
        """Проверить наличие заголовка модального окна amenities."""
        return self.amenities.verify_amenities_modal_title()

    def verify_amenities_modal_close_button(self):
        """Проверить наличие кнопки закрытия модального окна amenities."""
        return self.amenities.verify_amenities_modal_close_button()

    def close_amenities_modal(self):
        """Закрыть модальное окно amenities."""
        return self.amenities.close_amenities_modal()

    def verify_amenities_slider_displayed(self):
        """Проверить отображение слайдера в модалке amenities."""
        return self.amenities.verify_amenities_slider_displayed()

    def verify_amenities_slider_images(self):
        """Проверить наличие изображений в слайдере amenities."""
        return self.amenities.verify_amenities_slider_images()

    def verify_amenities_slider_indicators(self):
        """Проверить наличие индикаторов слайдера amenities."""
        return self.amenities.verify_amenities_slider_indicators()

    def click_amenities_slider_indicator(self, index: int):
        """Кликнуть на индикатор слайдера amenities по индексу."""
        return self.amenities.click_amenities_slider_indicator(index)

    def click_amenities_slider_next(self):
        """Кликнуть на кнопку 'Вперед' слайдера amenities."""
        return self.amenities.click_amenities_slider_next()

    def click_amenities_slider_prev(self):
        """Кликнуть на кнопку 'Назад' слайдера amenities."""
        return self.amenities.click_amenities_slider_prev()

    def verify_amenities_modal_closed(self):
        """Проверить, что модальное окно amenities закрылось."""
        return self.amenities.verify_amenities_modal_closed()

    # Методы для работы с 360 Area Tour (делегируются к area_tour_360)
    def click_360_area_tour_button(self):
        """Кликнуть на кнопку 360 Area Tour."""
        return self.area_tour_360.click_360_area_tour_button()

    def verify_360_area_tour_modal_displayed(self):
        """Проверить отображение модального окна 360 Area Tour."""
        return self.area_tour_360.verify_360_area_tour_modal_displayed()

    def verify_360_area_tour_content(self):
        """Проверить наличие контента в модальном окне 360 Area Tour."""
        return self.area_tour_360.verify_360_area_tour_content()

    def close_360_area_tour_modal(self):
        """Закрыть модальное окно 360 Area Tour."""
        return self.area_tour_360.close_360_area_tour_modal()

    # Методы для работы с Elire (делегируются к elire)
    def click_on_residences_button(self):
        """Кликнуть на кнопку Residences."""
        return self.elire.click_on_residences_button()

    def click_on_residences_button_and_request_viewing_form(self):
        """Кликнуть на кнопку Residences и открыть форму Request Viewing."""
        return self.elire.click_on_residences_button_and_request_viewing_form()

    def click_on_start3d_expansion_button(self):
        """Кликнуть на кнопку Start 3D Expansion."""
        return self.elire.click_on_start3d_expansion_button()

    # Методы для работы с проектами (делегируются к project)
    def click_available_apartment(
        self, apartment_selector: str = None, max_attempts: int = 10
    ) -> bool:
        """Найти и кликнуть на первый доступный апартамент на плане этажа."""
        return self.project.click_available_apartment(apartment_selector, max_attempts)

    def handle_auth_modal_if_present(self):
        """Обработать модальное окно авторизации, если оно появилось."""
        import os

        # Проверяем, появилось ли модальное окно авторизации
        if self.is_visible(".ant-modal-content", timeout=5000):
            # Получаем логин и пароль из переменных окружения
            username = os.getenv("USERNAME_ELIRE")
            password = os.getenv("PASSWORD_ELIRE")

            if username and password:
                # Заполняем поле логина
                self.fill("#username", username)

                # Заполняем поле пароля
                self.fill("#password", password)

                # Кликаем на кнопку входа
                self.click("button[data-test-id='modal-form-primary-button']")

                # Ждем исчезновения модального окна или появления сообщения об ошибке
                try:
                    self.page.wait_for_selector(
                        ".ant-modal-content", state="hidden", timeout=15000
                    )
                except:
                    # Если модальное окно не закрылось, проверяем есть ли ошибка
                    error_elements = self.page.locator(
                        ".ant-message-error, .ant-form-item-explain-error"
                    )
                    if error_elements.count() > 0:
                        error_message = error_elements.text_content()
                        raise AssertionError(f"Ошибка авторизации: {error_message}")
                    else:
                        # Если нет ошибки, но модальное окно не закрылось, закрываем его вручную
                        self.click(".ant-modal-close")
                        self.page.wait_for_selector(
                            ".ant-modal-content", state="hidden", timeout=5000
                        )
            else:
                raise AssertionError(
                    "Не заданы переменные окружения USERNAME_ELIRE и PASSWORD_ELIRE"
                )

    # ==================== ВНУТРЕННИЕ КЛАССЫ ДЛЯ ОРГАНИЗАЦИИ МЕТОДОВ ====================

    class MapNavigation:
        """Методы для навигации по карте и проектам."""

        def __init__(self, parent):
            self.parent = parent

        def wait_for_map_and_projects_loaded(self):
            """Ожидать полной загрузки карты и проектов."""
            try:
                # Сначала ждем загрузки контейнера карты
                self.parent.wait_for_element(
                    self.parent.locators.MAP_CONTAINER,
                    timeout=self.parent.MAP_LOAD_TIMEOUT,
                )

                # Затем ждем появления хотя бы одного проекта
                self.parent.page.wait_for_selector(
                    self.parent.locators.ALL_PROJECTS_SELECTOR,
                    state="visible",
                    timeout=self.parent.MAP_LOAD_TIMEOUT,
                )

                # Дополнительная пауза для стабилизации карты
                self.parent.page.wait_for_timeout(2000)

            except Exception as e:
                print(f"Ошибка при ожидании загрузки карты: {e}")

        def check_map_loaded(self):
            """Проверить загрузку карты."""
            self.parent.expect_visible(self.parent.locators.MAP_CONTAINER)

        def click_project(self, project_name: str):
            """Кликнуть по проекту на карте по названию."""
            # Получаем правильный локатор для проекта
            selector = self.parent._get_project_selector(project_name)

            # Ждем появления проекта
            self.parent.page.wait_for_selector(selector, state="visible", timeout=10000)

            # Для изображений на карте используем force_click из-за блокировки Google Maps
            if project_name.lower() == "peylaa" and "img" in selector:
                element = self.parent.page.locator(selector)
                element.click(force=True)
            else:
                self.parent.click(selector)

        def click_project_on_map(self, project_name: str):
            """Кликнуть на проект и затем на кнопку Explore Project."""
            self.wait_for_map_and_projects_loaded()

            # Проверяем, что проект найден на карте перед кликом
            selector = self.parent._get_project_selector(project_name)
            project_element = self.parent.page.locator(selector)
            assert (
                project_element.count() > 0
            ), f"Проект '{project_name}' не найден на карте - баг в UI"

            # Сначала кликаем на проект
            self.click_project(project_name)

            # Проверяем, что появилось окно с информацией о проекте
            self.parent.expect_visible(self.parent.locators.PROJECT_INFO_WINDOW)

            # Ждем появления кнопки Explore Project и проверяем её готовность
            explore_button = self.parent.wait_for_element(
                self.parent.locators.EXPLORE_PROJECT_BUTTON
            )
            assert (
                explore_button.is_enabled()
            ), f"Кнопка Explore Project заблокирована для проекта '{project_name}' - баг в UI"

            # Затем кликаем на кнопку Explore Project
            explore_button.click()

            # Ждем изменения URL (универсально для всех типов страниц)
            self.parent.page.wait_for_url(
                self.parent.project_locators.PROJECT_URL_PATTERN, timeout=10000
            )

        def check_project_info_visible(self, project_name: str):
            """Проверить видимость информации о проекте."""
            self.parent.expect_visible(self.parent.locators.PROJECT_INFO_WINDOW)

        def check_project_page_loaded(self, project_name: str):
            """Проверить загрузку страницы проекта."""
            # Находим проект по имени
            project = None
            for p in self.parent.project_locators.ALL_PROJECTS:
                if p.PROJECT_NAME == project_name.lower():
                    project = p
                    break

            if not project:
                raise ValueError(f"Неизвестный проект: {project_name}")

            # Проверяем, что мы на странице проекта (URL содержит /project/ и название проекта)
            current_url = self.parent.page.url
            self.parent.wait_for_page_load()
            assert (
                f"/project/{project.PROJECT_NAME}" in current_url
            ), f"Не на странице проекта {project.PROJECT_DISPLAY_NAME}. Текущий URL: {current_url}"

        def return_to_map_from_project_and_verify_returned_to_map(self):
            """Вернуться на карту из проекта и проверить, что мы на карте."""
            self.parent.page.go_back()
            self.check_map_loaded()

    class ProjectPage:
        """Методы для работы с проектами."""

        def __init__(self, parent):
            self.parent = parent

        def click_available_apartment(
            self, apartment_selector: str = None, max_attempts: int = 10
        ) -> bool:
            """
            Найти и кликнуть на первый доступный апартамент на плане этажа.

            Args:
                apartment_selector: Селектор для поиска апартаментов (по умолчанию из project_locators)
                max_attempts: Максимальное количество попыток клика

            Returns:
                bool: True если удалось кликнуть на апартамент
            """
            if apartment_selector is None:
                apartment_selector = self.parent.project_locators.FLOOR_PLAN_APARTMENTS

            # Ждем загрузки апартаментов
            self.parent.page.wait_for_selector(apartment_selector, timeout=10000)

            apartment_elements = self.parent.page.locator(apartment_selector)
            apartment_count = apartment_elements.count()

            if apartment_count == 0:
                return False

            # Ищем первый доступный апартамент (без замка)
            for i in range(min(apartment_count, max_attempts)):
                try:
                    apartment = apartment_elements.nth(i)

                    # Проверяем, есть ли замок
                    lock_icon = apartment.locator(
                        "xpath=.//span[@role='img' and @aria-label='lock']"
                    )
                    has_lock = lock_icon.count() > 0

                    if not has_lock:
                        apartment.click()
                        self.parent.page.wait_for_timeout(2000)

                        # Проверяем, перешли ли мы на страницу апартамента
                        current_url = self.parent.page.url
                        if "/apartment/" in current_url or "/unit/" in current_url:
                            return True

                except Exception:
                    continue

            return False

        # ==================== МЕТОДЫ ИЗ AGENT_PAGE ====================

        def click_on_download_pdf_button(self):
            """Кликает на кнопку скачивания PDF."""
            self.parent.click(
                self.parent.project_locators.DOWNLOAD_PDF_BUTTON, timeout=20000
            )

        def download_pdf_and_verify(self) -> tuple[bool, str]:
            """
            Скачать PDF в директорию и проверить что файл не пустой.

            Returns:
                tuple: (успех, путь к файлу)
            """
            import os
            import time

            try:
                # Создаем директорию для скачиваний
                download_dir = "temp/downloads"
                os.makedirs(download_dir, exist_ok=True)

                # Засекаем время начала скачивания
                start_time = time.time()

                # Начинаем скачивание с таймаутом 20 секунд
                with self.parent.page.expect_download(timeout=20000) as download_info:
                    # Кликаем по кнопке Download PDF с увеличенным таймаутом
                    self.parent.click(
                        self.parent.project_locators.DOWNLOAD_PDF_BUTTON, timeout=20000
                    )

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
            import os

            os.system("rm -rf temp")

        def click_on_all_units_button(self):
            """Кликнуть на кнопку All units."""
            self.parent.click(self.parent.project_locators.ALL_UNITS_BUTTON)

            # Ждем изменения URL на catalog_2d
            self.parent.page.wait_for_url("**/catalog_2d", timeout=10000)

        def find_and_click_available_apartment(self, project_name: str = None):
            """
            Найти и кликнуть на первый доступный апартамент (без замка).

            Args:
                project_name: Название проекта (используется только для логирования)
            """

            self.parent.page.wait_for_timeout(3500)

            # Ищем все апартаменты
            apartment_titles = self.parent.page.locator(
                self.parent.project_locators.ALL_APARTMENT_TITLES
            )
            apartment_count = apartment_titles.count()

            # Проверяем, что апартаменты найдены на странице
            assert (
                apartment_count > 0
            ), f"Апартаменты не найдены на странице - {project_name or 'неизвестный'}"

            # Ищем первый доступный апартамент (без замка)
            for i in range(apartment_count):
                apartment_title = apartment_titles.nth(i)

                # Сразу проверяем видимость без ожидания
                if not apartment_title.is_visible():
                    continue

                # Проверяем, есть ли замок у этого апартамента
                lock_icon = apartment_title.locator(
                    "xpath=.//span[@role='img' and @aria-label='lock']"
                )
                has_lock = lock_icon.count() > 0

                apartment_text = apartment_title.text_content()

                if not has_lock:
                    apartment_title.click(force=True)
                    return apartment_text

            # Если не найден ни один доступный апартамент
            raise AssertionError(
                f"Не найден ни один доступный апартамент для проекта {project_name}"
            )

        def click_on_sales_offer_button(self):
            """Кликнуть на кнопку Sales Offer."""
            self.parent.click(self.parent.project_locators.SALES_OFFER_BUTTON)

        # ==================== МЕТОДЫ ИЗ CLIENT_PAGE ====================

        def click_on_residences_button_and_request_viewing_form(self):
            """Кликает на кнопку Residences и открывает форму Request Viewing."""
            # Используем методы из внутреннего класса Elire
            self.parent.elire.click_on_residences_button_and_request_viewing_form()

        def fill_and_submit_request_viewing_form(self, fake):
            """Заполняет форму Request Viewing.

            Args:
                fake: Faker объект для генерации тестовых данных
            """
            self.parent.fill(
                self.parent.project_locators.Elire.FIRST_NAME_FIELD, fake.first_name()
            )
            self.parent.fill(
                self.parent.project_locators.Elire.LAST_NAME_FIELD, fake.last_name()
            )
            self.parent.fill(
                self.parent.project_locators.Elire.PHONE_FIELD, "+79999999999"
            )
            self.parent.fill(
                self.parent.project_locators.Elire.EMAIL_FIELD, fake.email()
            )
            self.parent.fill(self.parent.project_locators.Elire.NOTE_FIELD, fake.text())
            self.parent.click(
                self.parent.project_locators.Elire.SUBMIT_BUTTON_FOR_REQUEST_VIEWING
            )

        def is_success_message_displayed(self) -> bool:
            """
            Проверяет, отображается ли сообщение об успешной отправке.

            Returns:
                bool: True если сообщение об успехе отображается
            """
            # Проверяем модальное окно
            modal = self.parent.page.locator(
                self.parent.project_locators.Elire.SUCCESS_MODAL
            )

            if modal.is_visible():
                # Получаем весь текст модального окна
                modal_text = modal.text_content()

                # Проверяем наличие нужных текстов
                has_thank_you = "Thank you!" in modal_text
                has_contact_text = (
                    "Our specialist will contact you shortly." in modal_text
                )

                if has_thank_you and has_contact_text:
                    return True
            return False

    class Amenities:
        """Методы для работы с amenities."""

        def __init__(self, parent):
            self.parent = parent

        def click_explore_amenities_button(self):
            """Кликнуть на кнопку Explore Amenities."""
            self.parent.click(self.parent.project_locators.EXPLORE_AMENITIES_BUTTON)

        def verify_amenities_modal_displayed(self):
            """Проверить отображение модального окна amenities."""
            self.parent.expect_visible(self.parent.project_locators.AMENITIES_MODAL)

        def verify_amenities_modal_title(self):
            """Проверить наличие заголовка модального окна."""
            self.parent.expect_visible(
                self.parent.project_locators.AMENITIES_MODAL_TITLE
            )

        def verify_amenities_modal_close_button(self):
            """Проверить наличие кнопки закрытия модального окна."""
            self.parent.expect_visible(
                self.parent.project_locators.AMENITIES_MODAL_CLOSE_BUTTON
            )

        def close_amenities_modal(self):
            """Закрыть модальное окно amenities."""
            self.parent.click(self.parent.project_locators.AMENITIES_MODAL_CLOSE_BUTTON)

        def verify_amenities_slider_displayed(self):
            """Проверить отображение слайдера amenities."""
            self.parent.expect_visible(self.parent.project_locators.AMENITIES_SLIDER)

        def verify_amenities_slider_images(self):
            """Проверить наличие изображений в слайдере amenities."""
            slider_images = self.parent.page.locator(
                self.parent.project_locators.AMENITIES_SLIDER_IMAGES
            )
            assert (
                slider_images.count() > 0
            ), "Изображения в слайдере amenities не найдены"

        def verify_amenities_slider_indicators(self):
            """Проверить наличие индикаторов слайдера amenities."""
            slider_indicators = self.parent.page.locator(
                self.parent.project_locators.AMENITIES_SLIDER_INDICATORS
            )
            assert (
                slider_indicators.count() > 0
            ), "Индикаторы слайдера amenities не найдены"

        def click_amenities_slider_indicator(self, index: int):
            """Кликнуть на индикатор слайдера amenities по индексу."""
            indicators = self.parent.page.locator(
                self.parent.project_locators.AMENITIES_SLIDER_INDICATORS
            )
            indicators.nth(index).click()

        def click_amenities_slider_next(self):
            """Кликнуть на кнопку 'следующий' слайдера amenities."""
            self.parent.click(self.parent.project_locators.AMENITIES_SLIDER_NEXT)

        def click_amenities_slider_prev(self):
            """Кликнуть на кнопку 'предыдущий' слайдера amenities."""
            self.parent.click(self.parent.project_locators.AMENITIES_SLIDER_PREV)

        def verify_amenities_modal_closed(self):
            """Проверить, что модальное окно amenities закрыто."""
            self.parent.page.wait_for_selector(
                self.parent.project_locators.AMENITIES_MODAL,
                state="hidden",
                timeout=5000,
            )

    class AreaTour360:
        """Методы для работы с 360 Area Tour."""

        def __init__(self, parent):
            self.parent = parent

        def click_360_area_tour_button(self):
            """Кликнуть на кнопку 360 Area Tour."""
            self.parent.click(self.parent.project_locators.AREA_TOUR_360_BUTTON)

        def verify_360_area_tour_modal_displayed(self):
            """Проверить отображение модального окна 360 Area Tour."""
            elem = self.parent.expect_visible(
                self.parent.project_locators.AREA_TOUR_360_MODAL
            )

        def verify_360_area_tour_content(self):
            """Проверить наличие контента в модальном окне 360 Area Tour."""
            # Проверяем наличие контента (изображения, видео или другие элементы)
            content_element = self.parent.page.locator(
                self.parent.project_locators.AREA_TOUR_360_CONTENT
            )
            assert (
                content_element.count() > 0
            ), "Контент 360 Area Tour не найден в модальном окне"

        def close_360_area_tour_modal(self):
            """Закрыть модальное окно 360 Area Tour."""
            # Ищем кнопку закрытия модального окна
            close_button = self.parent.page.locator(
                self.parent.project_locators.AREA_TOUR_360_CLOSE_BUTTON
            )
            if close_button.is_visible():
                close_button.click()
            else:
                # Если кнопки закрытия нет, нажимаем Escape
                self.parent.page.keyboard.press("Escape")

    class Elire:
        """Методы специфичные для проекта Elire."""

        def __init__(self, parent):
            self.parent = parent

        def click_on_residences_button(self):
            """Кликнуть на кнопку Residences."""
            self.parent.click(self.parent.project_locators.Elire.RESIDENCES_BUTTON)

        def click_on_residences_button_and_request_viewing_form(self):
            """Кликнуть на кнопку Residences и открыть форму Request Viewing."""
            self.parent.click(self.parent.project_locators.Elire.RESIDENCES_BUTTON)
            self.parent.click(self.parent.project_locators.Elire.REQUEST_VIEWING_BUTTON)

        def click_on_start3d_expansion_button(self):
            """Кликнуть на кнопку Start 3D Expansion."""
            self.parent.click(
                self.parent.project_locators.Elire.START_3D_EXPANSION_BUTTON
            )

        def click_on_services_amenities_button(self):
            self.parent.click(
                self.parent.project_locators.Elire.SERVICES_AMENITIES_BUTTON
            )

    class ApartmentWidget:
        """Класс для работы с виджетом апартамента."""

        def __init__(self, parent):
            self.parent = parent

        def open_apartment_page(self, project_name: str, apartment_id: str = "104"):
            """Открыть страницу апартамента.

            Args:
                project_name: Название проекта (arisha, elire, cubix)
                apartment_id: ID апартамента (по умолчанию 104)
            """
            # Получаем базовый URL из окружения
            from conftest import _get_urls_by_environment

            urls = _get_urls_by_environment()
            base_url = urls["map"].replace("/map", "")  # Убираем /map из базового URL

            apartment_url = (
                f"{base_url}/project/{project_name}/apartment/1/1/{apartment_id}"
            )
            self.parent.page.goto(apartment_url)
            self.parent.page.wait_for_load_state("domcontentloaded")

            # Ждем загрузки iframe с виджетом
            self.parent.page.wait_for_selector(
                "iframe[class*='_iframe_']", timeout=15000
            )
            # Ждем загрузки содержимого iframe
            iframe = self.parent.page.frame_locator("iframe[class*='_iframe_']")
            iframe.locator("body").wait_for(state="visible", timeout=15000)

        def get_widget_frame(self):
            """Получить frame_locator для виджета апартамента."""
            return self.parent.page.frame_locator("iframe[class*='_iframe_']")

        def switch_to_2d_mode(self, project_name: str):
            """Переключиться в режим 2D."""
            frame_locator = self.get_widget_frame()
            widget_locators = getattr(
                self.parent.project_locators, project_name.capitalize()
            ).ApartmentWidget()

            view_2d_button = frame_locator.locator(widget_locators.VIEW_2D_BUTTON)
            view_2d_button.wait_for(state="visible", timeout=15000)

            # Проверяем, что кнопка 2D не активна (если уже активна, то переключение не нужно)
            button_class = view_2d_button.get_attribute("class")
            if "active" in button_class:
                return  # Уже в режиме 2D

            view_2d_button.click()

            # Ждем, что кнопка 2D стала активной
            try:
                # Используем умный вейтер - ждем изменения атрибута class
                view_2d_button.wait_for(
                    lambda: "active" in view_2d_button.get_attribute("class") or "",
                    timeout=5000,
                )
            except Exception:
                # Fallback: проверяем класс кнопки напрямую
                button_class = view_2d_button.get_attribute("class")
                if "active" not in button_class:
                    raise Exception("Кнопка 2D не стала активной после клика")

            # Ждем появления стрелочек навигации в режиме 2D
            next_arrow = frame_locator.locator(widget_locators.NEXT_ARROW).first
            next_arrow.wait_for(state="visible", timeout=10000)

        def switch_to_3d_mode(self, project_name: str):
            """Переключиться в режим 3D."""
            frame_locator = self.get_widget_frame()
            widget_locators = getattr(
                self.parent.project_locators, project_name.capitalize()
            ).ApartmentWidget()

            view_3d_button = frame_locator.locator(widget_locators.VIEW_3D_BUTTON)
            view_3d_button.wait_for(state="visible", timeout=15000)

            # Проверяем, что кнопка 3D не активна (если уже активна, то переключение не нужно)
            button_class = view_3d_button.get_attribute("class")
            if "active" in button_class:
                return  # Уже в режиме 3D

            view_3d_button.click()

            # Ждем, что кнопка 3D стала активной
            try:
                # Используем умный вейтер - ждем изменения атрибута class
                view_3d_button.wait_for(
                    lambda: "active" in view_3d_button.get_attribute("class") or "",
                    timeout=5000,
                )
            except Exception:
                # Fallback: проверяем класс кнопки напрямую
                button_class = view_3d_button.get_attribute("class")
                if "active" not in button_class:
                    raise Exception("Кнопка 3D не стала активной после клика")

        def click_speed_button(self, project_name: str):
            """Кликнуть на кнопку скорости 0.5x."""
            frame_locator = self.get_widget_frame()
            widget_locators = getattr(
                self.parent.project_locators, project_name.capitalize()
            ).ApartmentWidget()

            speed_button = frame_locator.locator(widget_locators.SPEED_BUTTON)

            if speed_button.count() > 0 and speed_button.first.is_visible():
                speed_button.first.click()
                # Небольшая пауза после клика для стабилизации
                self.parent.page.wait_for_timeout(500)
                return True
            return False

        def navigate_to_next_slide(self, project_name: str, count: int = 1):
            """Перейти к следующему слайду.

            Args:
                project_name: Название проекта
                count: Количество слайдов для перехода
            """
            frame_locator = self.get_widget_frame()
            widget_locators = getattr(
                self.parent.project_locators, project_name.capitalize()
            ).ApartmentWidget()

            next_arrows = frame_locator.locator(widget_locators.NEXT_ARROW)
            scene_indicator = frame_locator.locator(widget_locators.SCENE_INDICATOR)

            scenes = []

            for i in range(count):
                if next_arrows.count() > 0:
                    next_arrow = next_arrows.first
                    if next_arrow.is_visible():
                        next_arrow.click()

                        # Небольшая пауза для стабилизации после клика
                        self.parent.page.wait_for_timeout(500)

                        # Ждем изменения сцены после клика
                        if scene_indicator.count() > 0:
                            scene_indicator.first.wait_for(
                                state="visible", timeout=2000
                            )

                        # Получаем текущую сцену
                        if scene_indicator.count() > 0:
                            current_scene = scene_indicator.first.text_content()
                            scenes.append(current_scene)

            return scenes

        def get_current_scene(self, project_name: str):
            """Получить текущую сцену."""
            frame_locator = self.get_widget_frame()
            widget_locators = getattr(
                self.parent.project_locators, project_name.capitalize()
            ).ApartmentWidget()

            scene_indicator = frame_locator.locator(widget_locators.SCENE_INDICATOR)

            if scene_indicator.count() > 0:
                return scene_indicator.first.text_content()
            return None

        def check_navigation_arrows_visible(self, project_name: str):
            """Проверить видимость стрелочек навигации."""
            frame_locator = self.get_widget_frame()
            widget_locators = getattr(
                self.parent.project_locators, project_name.capitalize()
            ).ApartmentWidget()

            prev_arrows = frame_locator.locator(widget_locators.PREV_ARROW)
            next_arrows = frame_locator.locator(widget_locators.NEXT_ARROW)

            prev_visible = prev_arrows.count() > 0 and prev_arrows.first.is_visible()
            next_visible = next_arrows.count() > 0 and next_arrows.first.is_visible()

            return prev_visible and next_visible

        def check_navigation_arrows_hidden(self, project_name: str):
            """Проверить, что стрелочки навигации скрыты."""
            frame_locator = self.get_widget_frame()
            widget_locators = getattr(
                self.parent.project_locators, project_name.capitalize()
            ).ApartmentWidget()

            prev_arrows = frame_locator.locator(widget_locators.PREV_ARROW)
            next_arrows = frame_locator.locator(widget_locators.NEXT_ARROW)

            prev_hidden = prev_arrows.count() == 0 or not prev_arrows.first.is_visible()
            next_hidden = next_arrows.count() == 0 or not next_arrows.first.is_visible()

            return prev_hidden and next_hidden

        def check_mode_button_active(self, project_name: str, mode: str):
            """Проверить, что кнопка режима активна.

            Args:
                project_name: Название проекта
                mode: Режим ('2D' или '3D')
            """
            frame_locator = self.get_widget_frame()
            widget_locators = getattr(
                self.parent.project_locators, project_name.capitalize()
            ).ApartmentWidget()

            if mode == "2D":
                button = frame_locator.locator(widget_locators.VIEW_2D_BUTTON)
            elif mode == "3D":
                button = frame_locator.locator(widget_locators.VIEW_3D_BUTTON)
            else:
                raise ValueError(f"Неизвестный режим: {mode}")

            button_class = button.get_attribute("class")
            return "active" in button_class if button_class else False

        def take_widget_screenshot(self):
            """Сделать скриншот виджета."""
            iframe_element = self.parent.page.locator("iframe")
            return iframe_element.screenshot()

    class ApartmentInfo:
        """Класс для работы с информацией об апартаменте."""

        def __init__(self, parent):
            self.parent = parent

        def wait_for_info_to_appear(self, project_name: str):
            """Дождаться появления информации об апартаменте."""
            info_locators = getattr(
                self.parent.project_locators, project_name.capitalize()
            ).ApartmentInfo()
            self.parent.page.wait_for_selector(
                info_locators.INFO_CONTAINER, timeout=10000
            )

        def check_apartment_number(
            self, project_name: str, apartment_number: str = "104"
        ):
            """Проверить номер апартамента."""
            info_locators = getattr(
                self.parent.project_locators, project_name.capitalize()
            ).ApartmentInfo()
            apartment_element = self.parent.page.locator(
                info_locators.APARTMENT_NUMBER
            ).first
            apartment_text = apartment_element.text_content()
            return f"APT. {apartment_number}" in apartment_text

        def check_apartment_type(self, project_name: str):
            """Проверить тип апартамента."""
            info_locators = getattr(
                self.parent.project_locators, project_name.capitalize()
            ).ApartmentInfo()
            type_element = self.parent.page.locator(info_locators.TYPE_VALUE).first
            return type_element.is_visible()

        def check_floor_info(self, project_name: str):
            """Проверить информацию о этаже (опционально)."""
            info_locators = getattr(
                self.parent.project_locators, project_name.capitalize()
            ).ApartmentInfo()
            floor_element = self.parent.page.locator(info_locators.FLOOR_VALUE).first
            return floor_element.is_visible()

        def check_building_info(self, project_name: str):
            """Проверить информацию о здании."""
            info_locators = getattr(
                self.parent.project_locators, project_name.capitalize()
            ).ApartmentInfo()
            building_element = self.parent.page.locator(
                info_locators.BUILDING_VALUE
            ).first
            return building_element.is_visible()

        def check_area_info(self, project_name: str):
            """Проверить информацию о площади."""
            info_locators = getattr(
                self.parent.project_locators, project_name.capitalize()
            ).ApartmentInfo()
            area_element = self.parent.page.locator(info_locators.AREA_VALUE).first
            return area_element.is_visible()

        def check_view_info(self, project_name: str):
            """Проверить информацию о виде."""
            info_locators = getattr(
                self.parent.project_locators, project_name.capitalize()
            ).ApartmentInfo()
            view_element = self.parent.page.locator(info_locators.VIEW_VALUE).first
            return view_element.is_visible()

        def check_features(self, project_name: str):
            """Проверить наличие особенностей апартамента."""
            info_locators = getattr(
                self.parent.project_locators, project_name.capitalize()
            ).ApartmentInfo()

            features = {
                "modern_design": self.parent.page.locator(
                    info_locators.MODERN_DESIGN
                ).first.is_visible(),
                "high_quality": self.parent.page.locator(
                    info_locators.HIGH_QUALITY
                ).first.is_visible(),
                "built_in_appliances": self.parent.page.locator(
                    info_locators.BUILT_IN_APPLIANCES
                ).first.is_visible(),
            }
            return features

        def check_watching_count(self, project_name: str):
            """Проверить счетчик просмотров."""
            info_locators = getattr(
                self.parent.project_locators, project_name.capitalize()
            ).ApartmentInfo()
            watching_element = self.parent.page.locator(
                info_locators.WATCHING_COUNT
            ).first
            return watching_element.is_visible()

        def get_info_text(self, project_name: str):
            """Получить весь текст информации об апартаменте."""
            info_locators = getattr(
                self.parent.project_locators, project_name.capitalize()
            ).ApartmentInfo()
            info_element = self.parent.page.locator(info_locators.INFO_CONTAINER).first
            return info_element.text_content()

        def take_info_screenshot(self, project_name: str):
            """Сделать скриншот информации об апартаменте."""
            info_locators = getattr(
                self.parent.project_locators, project_name.capitalize()
            ).ApartmentInfo()
            info_element = self.parent.page.locator(info_locators.INFO_CONTAINER).first
            return info_element.screenshot()
