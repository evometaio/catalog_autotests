import time

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

    # Константы для таймаутов (оптимизированы)
    DEFAULT_TIMEOUT = 10000  # Оптимизировано с 20000
    LONG_TIMEOUT = 15000  # Оптимизировано с 30000
    SHORT_TIMEOUT = 5000
    MAP_LOAD_TIMEOUT = 20000  # Оптимизировано с 30000

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
        element.wait_for(state="visible", timeout=timeout)
        return element

    def get_current_url(self) -> str:
        """Получить текущий URL."""
        return self.page.url

    def get_project_url(self, project_name: str, page_type: str = "catalog2d") -> str:
        """Получить URL для конкретного проекта и типа страницы.

        Args:
            project_name: Название проекта (arisha, cubix, elire, peylaa, tranquil)
            page_type: Тип страницы (catalog2d, area, map)

        Returns:
            str: URL для проекта
        """
        from conftest import _get_urls_by_environment

        urls = _get_urls_by_environment()
        project_name_lower = project_name.lower()

        # Проверяем валидность типа страницы
        if page_type not in self.project_locators.PAGE_TYPES:
            raise ValueError(f"Неизвестный тип страницы: {page_type}")

        # Определяем базовый URL в зависимости от проекта
        if project_name_lower in self.project_locators.QUBE_PROJECTS:
            # Qube проекты
            base_url = urls["map"].replace("/map", "")
        elif project_name_lower in self.project_locators.CAPSTONE_PROJECTS:
            # Capstone проект
            base_url = urls["capstone_map"].replace("/map", "")
        elif project_name_lower in self.project_locators.WELLCUBE_PROJECTS:
            # Wellcube проект
            base_url = urls["wellcube_map"].replace("/map", "")
        else:
            raise ValueError(f"Неизвестный проект: {project_name}")

        # Формируем полный URL
        if page_type == "catalog2d":
            return f"{base_url}/project/{project_name_lower}/catalog_2d"
        elif page_type == "area":
            return f"{base_url}/project/{project_name_lower}/area"
        elif page_type == "map":
            return urls.get(f"{project_name_lower}_map", urls["map"])

    def click(self, selector: str, timeout: int = None):
        """Кликнуть по элементу."""
        element = self.wait_for_element(selector, timeout)
        expect(element).to_be_enabled()
        expect(element).to_be_visible()
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
        expect(element).to_be_visible()

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
        project_name_lower = project_name.lower()

        # Получаем проект из локаторов
        project_class = self._get_project_class(project_name_lower)
        if not project_class:
            # Fallback на старый способ
            return f'div[aria-label*="{project_name}"], div[aria-label*="{project_name.upper()}"]'

        # Для Peylaa учитываем окружение
        if project_name_lower == "peylaa":
            import os

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
        self.expect_visible(self.project_locators.ALL_UNITS_BUTTON)
        self.click(self.project_locators.ALL_UNITS_BUTTON)

    def click_on_sales_offer_button(self):
        """Кликнуть на кнопку Sales Offer."""
        self.expect_visible(self.project_locators.SALES_OFFER_BUTTON)
        self.click(self.project_locators.SALES_OFFER_BUTTON)

    # Методы для работы с 360 Area Tour (перенесены в AreaTour360 класс)

    # Методы для инкапсуляции работы с page
    def click_element(self, selector: str):
        """Кликнуть по элементу по селектору."""
        self.page.click(selector)

    def query_selector_all(self, selector: str):
        """Найти все элементы по селектору."""
        return self.page.query_selector_all(selector)

    def wait_for_timeout(self, timeout: int):
        """Ждать указанное количество миллисекунд."""
        self.page.wait_for_timeout(timeout)

    def is_element_visible(self, selector: str, timeout: int = 5000) -> bool:
        """Проверить, виден ли элемент."""
        try:
            element = self.page.locator(selector)
            return element.is_visible(timeout=timeout)
        except:
            return False

    def get_element_text(self, selector: str) -> str:
        """Получить текст элемента."""
        return self.page.locator(selector).text_content()

    def get_element_count(self, selector: str) -> int:
        """Получить количество элементов по селектору."""
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
            # Сначала кликаем на проект
            self.click_project(project_name)

            # Для остальных случаев ищем кнопку Explore Project
            self.parent.expect_visible(self.parent.locators.PROJECT_INFO_WINDOW)
            self.parent.expect_visible(self.parent.locators.EXPLORE_PROJECT_BUTTON)

            # Затем кликаем на кнопку Explore Project
            self.parent.click(self.parent.locators.EXPLORE_PROJECT_BUTTON)

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
            self.parent.expect_visible(self.parent.project_locators.AREA_TOUR_360_MODAL)

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
            self.parent.expect_visible(
                self.parent.project_locators.Elire.RESIDENCES_BUTTON
            )
            self.parent.click(self.parent.project_locators.Elire.RESIDENCES_BUTTON)

        def click_on_residences_button_and_request_viewing_form(self):
            """Кликнуть на кнопку Residences и открыть форму Request Viewing."""
            self.parent.expect_visible(
                self.parent.project_locators.Elire.RESIDENCES_BUTTON
            )
            self.parent.click(self.parent.project_locators.Elire.RESIDENCES_BUTTON)
            self.parent.click(self.parent.project_locators.Elire.REQUEST_VIEWING_BUTTON)

        def click_on_start3d_expansion_button(self):
            """Кликнуть на кнопку Start 3D Expansion."""
            self.parent.expect_visible(
                self.parent.project_locators.Elire.START_3D_EXPANSION_BUTTON
            )
            self.parent.click(
                self.parent.project_locators.Elire.START_3D_EXPANSION_BUTTON
            )
