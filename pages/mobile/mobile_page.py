import allure
from playwright.sync_api import Locator, Page

from locators.mobile_locators import *
from pages.components.apartment_widget_component import ApartmentWidgetComponent
from pages.components.area_tour_360_component import AreaTour360Component
from pages.core.assertions import Assertions
from pages.core.browser_actions import BrowserActions

from ..base_page import BasePage
from .mobile_components.mobile_map_component import MobileMapComponent
from .mobile_components.mobile_navigation_component import MobileNavigationComponent


class MobilePage(BasePage):
    """Мобильная версия BasePage с адаптивными методами."""

    def __init__(self, page: Page):
        # Устанавливаем базовые URL-ы для разных окружений
        import os

        environment = os.getenv("TEST_ENVIRONMENT", "dev")
        if environment == "dev":
            base_url = os.getenv(
                "DEV_AGENT_BASE_URL", "https://qube-dev-next.evometa.io/agent/map"
            )
            self.agent_base_url = os.getenv(
                "DEV_AGENT_BASE_URL", "https://qube-dev-next.evometa.io/agent/map"
            )
            self.client_base_url = os.getenv(
                "DEV_CLIENT_BASE_URL", "https://qube-dev-next.evometa.io/client/map"
            )
        else:
            base_url = os.getenv(
                "AGENT_PROD_BASE_URL", "https://virtualtours.qbd.ae/agent/map"
            )
            self.agent_base_url = os.getenv(
                "AGENT_PROD_BASE_URL", "https://virtualtours.qbd.ae/agent/map"
            )
            self.client_base_url = os.getenv(
                "CLIENT_PROD_BASE_URL", "https://virtualtours.qbd.ae/client/map"
            )

        # Инициализируем BasePage с правильным URL
        super().__init__(page, base_url)
        self.device_type = "mobile"

        # Инициализируем мобильные компоненты
        self.mobile_map = MobileMapComponent(page)
        self.mobile_navigation = MobileNavigationComponent(page)

        # Добавляем desktop компоненты которые работают и на мобилке
        self.area_tour_360 = AreaTour360Component(page, self.project_locators)
        # apartment_widget будет инициализирован после установки project_name
        self.apartment_widget = None

        # Переопределяем browser и assertions если они не были созданы в BasePage
        if not hasattr(self, "browser"):
            self.browser = BrowserActions(page)
        if not hasattr(self, "assertions"):
            self.assertions = Assertions(page)

    # ==================== МОБИЛЬНЫЕ ЛОКАТОРЫ ====================
    # Все локаторы теперь импортируются из locators/mobile_locators.py

    # ==================== МОБИЛЬНЫЕ МЕТОДЫ ДЛЯ КАРТЫ ====================

    def click_360_area_tour_button(self):
        """Кликнуть на кнопку 360 Area Tour для мобильных устройств (второй элемент)."""
        with allure.step("Кликаем на кнопку 360 Area Tour"):
            button_selector = (
                '(//button[@data-test-id="nav-rotation-view-controls-button"])[2]'
            )
            button = self.page.locator(button_selector)
            button.wait_for(state="visible", timeout=10000)
            button.click()

    def click_mobile_explore_residences_button(self):
        """Кликнуть на кнопку Explore Residences для Elire (второй элемент)."""
        with allure.step("Кликаем на Explore Residences"):
            button = self.page.locator('button:has-text("explore residences")').nth(1)
            button.wait_for(state="visible", timeout=10000)
            button.click()

    def click_mobile_start_3d_experience_button(self):
        """Кликнуть на кнопку Start 3D Experience для Elire."""
        with allure.step("Кликаем на Start 3D Experience"):
            button = self.page.locator(
                '[data-test-id="property-info-primary-button-1 BEDROOM RESIDENCE"]'
            ).first
            button.wait_for(state="visible", timeout=10000)
            button.click()

    def click_mobile_services_amenities_button(self):
        """Кликнуть на кнопку Services & Amenities для Elire."""
        with allure.step("Кликаем на Services & Amenities"):
            button = self.page.locator('button:has-text("services & amenities")')
            button.wait_for(state="visible", timeout=10000)
            button.click()

    def navigate_to_mobile_arisha_all_units(self):
        """Навигация к All Units через мобильное меню для Arisha."""
        with allure.step("Открываем мобильное меню Arisha"):
            mobile_menu_toggle = self.page.locator(
                '[data-test-id="nav-mobile-menu-toggle"]'
            )
            mobile_menu_toggle.wait_for(state="visible", timeout=10000)
            mobile_menu_toggle.click()

        with allure.step("Кликаем на All Units в меню"):
            all_units_button = self.page.locator(
                '[data-test-id="nav-mobile-catalog2d"]'
            )
            all_units_button.wait_for(state="visible", timeout=10000)
            all_units_button.click()

    def click_on_fraction_ownership_offer_button(self):
        """Кликнуть на кнопку Fraction Ownership Offer для Tranquil."""
        with allure.step("Кликаем на кнопку Fraction Ownership Offer"):
            button = self.page.locator(
                '(//button[@data-test-id="property-info-primary-button-1102 A"])[1]'
            )
            button.first.click(force=True)

    def wait_for_apartment_widget_load(self):
        """Ожидание полной загрузки виджета апартамента."""
        with allure.step("Ожидаем полной загрузки виджета апартамента"):
            # Ждем появления iframe
            self.page.wait_for_selector("iframe[class*='_iframe_']", timeout=15000)
            # Ждем загрузки содержимого внутри iframe
            self.page.wait_for_timeout(4000)

    def verify_elire_services_modal_displayed(self):
        """Проверить отображение модального окна Services & Amenities для Elire."""
        with allure.step("Проверяем отображение модального окна Services & Amenities"):
            modal = self.page.locator(".ant-modal-content")
            modal.wait_for(state="visible", timeout=10000)
            assert (
                modal.is_visible()
            ), "Модальное окно Services & Amenities не отображается"

    def verify_elire_services_modal_title(self):
        """Проверить наличие заголовка CORE SERVICES."""
        with allure.step("Проверяем наличие заголовка CORE SERVICES"):
            title = self.page.locator('[data-test-id="public-zone-info-slider-title"]')
            assert title.is_visible(), "Заголовок CORE SERVICES не найден"

    def navigate_elire_services_slider(self):
        """Тестировать навигацию по слайдеру Services & Amenities."""
        with allure.step("Тестируем навигацию по слайдеру - кликаем вправо"):
            right_arrow = self.page.locator(
                '.ant-modal-content span[aria-label="right"]'
            )
            if right_arrow.count() > 0:
                for i in range(3):
                    right_arrow.first.click(force=True)
                    self.page.wait_for_timeout(800)

        with allure.step("Тестируем навигацию по слайдеру - кликаем влево"):
            left_arrow = self.page.locator('.ant-modal-content span[aria-label="left"]')
            if left_arrow.count() > 0:
                for i in range(2):
                    left_arrow.first.click(force=True)
                    self.page.wait_for_timeout(800)

    def close_elire_services_modal(self):
        """Закрыть модальное окно Services & Amenities."""
        with allure.step("Закрываем модальное окно"):
            close_button = self.page.locator(".ant-modal-close")
            close_button.click()
            modal = self.page.locator(".ant-modal-content")
            modal.wait_for(state="hidden", timeout=5000)

    # ==================== МЕТОДЫ КАРТЫ - ДЕЛЕГАТЫ К MOBILE_MAP ====================

    def get_mobile_project_selector(self, project_name: str) -> str:
        """Получить мобильный селектор для проекта."""
        return self.mobile_map.get_mobile_project_selector(project_name)

    def click_mobile_project_on_map(self, project_name: str):
        """Кликнуть по проекту на карте для мобильных устройств."""
        return self.mobile_map.click_project(project_name)

    def wait_for_mobile_project_modal(self):
        """Ждать появления мобильного модального окна."""
        return self.mobile_map.wait_for_project_modal()

    def click_mobile_explore_project_button(self, project_name: str):
        """Кликнуть по кнопке Explore Project."""
        return self.mobile_map.click_explore_project(project_name)

    def close_mobile_project_modal(self):
        """Закрыть мобильное модальное окно."""
        return self.mobile_map.close_project_modal()

    # ==================== МОБИЛЬНЫЕ МЕТОДЫ НАВИГАЦИИ ====================

    def navigate_to_mobile_project_from_map(self, project_name: str):
        """Полная навигация от карты до страницы проекта на мобильном устройстве."""
        with allure.step(
            f"Переходим от карты к проекту {project_name.upper()} на мобильном устройстве"
        ):
            # Открываем карту
            self.open(route_type="map")

            # Кликаем по проекту
            self.click_mobile_project_on_map(project_name)

            # Кликаем по кнопке Explore Project
            self.click_mobile_explore_project_button(project_name)

            # Проверяем успешность перехода
            current_url = self.page.url
            assert (
                f"/{project_name.lower()}/" in current_url
            ), f"Не удалось перейти к проекту {project_name}"

    def navigate_to_mobile_agent_page(self, project_name: str):
        """Переход на страницу агента для мобильных устройств."""
        with allure.step(f"Переходим на страницу агента {project_name.upper()}"):
            # Сначала переходим на страницу проекта
            self.navigate_to_mobile_project_from_map(project_name)

            # Ищем ссылку на агента
            agent_selectors = [
                f'a[href*="/{project_name.lower()}/agent/"]',
                'button:has-text("Agent")',
                'a:has-text("Agent")',
                '[data-testid*="agent"]',
            ]

            agent_link = None
            for selector in agent_selectors:
                elements = self.page.locator(selector)
                if elements.count() > 0 and elements.first.is_visible():
                    agent_link = elements.first
                    break

            if agent_link:
                agent_link.click()
                self.page.wait_for_load_state("domcontentloaded")
            else:
                # Если нет прямой ссылки, переходим по правильному URL агента
                agent_url = f"{self.agent_base_url}/{project_name.lower()}/"
                self.page.goto(agent_url)
                self.page.wait_for_load_state("domcontentloaded")

    def navigate_to_mobile_catalog_page(self, project_name: str):
        """Переход на страницу каталога через полную навигацию для мобильных устройств."""
        with allure.step(
            f"Переходим на страницу каталога {project_name.upper()} через полную навигацию"
        ):
            # 1. Переходим на карту
            # Для Arsenal используем специальный URL, для остальных - agent URL
            if project_name.lower() == "arsenal":
                # Для Arsenal используем прямой URL из conftest
                from conftest import _get_urls_by_environment

                urls = _get_urls_by_environment()
                arsenal_url = urls.get("vibe_arsenal", urls.get("map"))
                self.page.goto(arsenal_url)
            else:
                # Для остальных проектов используем agent URL
                self.page.goto(self.agent_base_url)
            self.page.wait_for_load_state("domcontentloaded")

            # 2. Кликаем по проекту на карте
            self.click_mobile_project_on_map(project_name)

            # 3. Кликаем на "Explore Project"
            self.click_mobile_explore_project_button(project_name)

            # 4. Кликаем на кнопку проекта для открытия меню
            if project_name.lower() == "arisha":
                arisha_button = self.page.locator(MOBILE_ARISHA_MENU_BUTTON)
                arisha_button.wait_for(state="visible", timeout=10000)
                arisha_button.click()
                self.page.wait_for_timeout(1000)  # Ждем открытия меню

                # 5. Кликаем на "ALL UNITS"
                all_units_button = self.page.locator(MOBILE_ALL_UNITS_BUTTON)
                all_units_button.wait_for(state="visible", timeout=10000)
                all_units_button.click()

                # 6. Ждем перехода на страницу каталога
                self.page.wait_for_url("**/catalog_2d", timeout=10000)
            elif project_name.lower() == "cubix":
                cubix_button = self.page.locator(MOBILE_CUBIX_MENU_BUTTON)
                cubix_button.wait_for(state="visible", timeout=10000)
                cubix_button.click()

                # 5. Для Cubix клик на кнопку сразу переводит на страницу каталога
                # Ждем перехода на страницу каталога
                self.page.wait_for_url("**/catalog_2d", timeout=10000)
            elif project_name.lower() == "arsenal":
                # Для Arsenal на мобильном нужно открыть меню, затем кликнуть на ALL UNITS
                # 1. Кликаем на кнопку меню
                menu_button = self.page.locator(
                    '[data-test-id="nav-mobile-menu-toggle"]'
                )
                menu_button.wait_for(state="visible", timeout=10000)
                menu_button.click()
                self.page.wait_for_timeout(1000)  # Ждем открытия меню

                # 2. Кликаем на ALL UNITS в меню
                all_units_button = self.page.locator(
                    '[data-test-id="nav-mobile-catalog2d"]'
                )
                all_units_button.wait_for(state="visible", timeout=10000)
                all_units_button.click()

                # Ждем перехода на страницу каталога
                self.page.wait_for_url("**/catalog_2d", timeout=10000)
            else:
                # Для других проектов может потребоваться другая логика
                raise NotImplementedError(
                    f"Навигация к каталогу для проекта {project_name} не реализована"
                )

    def click_mobile_explore_amenities_button(self):
        """Кликнуть на кнопку Explore Amenities для мобильных устройств."""
        # Для мобильных версий Arisha и Cubix корректен первый экземпляр кнопки
        # Explore Amenities, поэтому используем явный индекс [1], чтобы
        # избежать strict mode violation при наличии дубликатов.
        mobile_amenities_button = (
            '(//button[@data-test-id="project-info-window-explore-amenities"])[1]'
        )
        self.browser.click(mobile_amenities_button)

    def click_mobile_amenities_next_button(self):
        """Кликнуть на стрелку 'вправо' в слайдере amenities на мобильном."""
        next_button_selector = '.ant-modal-content span[aria-label="right"]'
        next_button = self.page.locator(next_button_selector)
        next_button.click()

    def click_mobile_download_pdf_button(self):
        """Кликнуть на кнопку Download PDF на мобильном устройстве."""
        with allure.step("Кликаем на Download PDF"):
            self.browser.click(MOBILE_DOWNLOAD_PDF_BUTTON)

    def find_and_click_available_apartment(self):
        """Найти и кликнуть на первый доступный apartment."""
        return self.mobile_navigation.find_and_click_available_apartment()

    def click_mobile_pdf_button(self):
        """Кликнуть по PDF кнопке на мобильном устройстве."""
        with allure.step("Ищем и кликаем по PDF кнопке"):
            # Ищем PDF кнопку через иконку
            pdf_icons = self.page.locator(MOBILE_PDF_BUTTON)

            if pdf_icons.count() == 0:
                raise AssertionError("PDF кнопка не найдена")

            for i in range(pdf_icons.count()):
                icon = pdf_icons.nth(i)
                if icon.is_visible():
                    # Получаем родительский элемент (кнопку)
                    parent_button = icon.locator("xpath=..").first
                    parent_tag = parent_button.evaluate("el => el.tagName")

                    if parent_tag.lower() == "button":
                        with allure.step(f"Кликаем на PDF кнопку {i+1}"):
                            parent_button.click()
                            self.page.wait_for_timeout(MOBILE_TIMEOUTS["medium"])

                            # Проверяем, появился ли диалог скачивания
                            download_dialogs = self.page.locator(
                                'dialog, [role="dialog"]'
                            )
                            if download_dialogs.count() > 0:
                                with allure.step("Диалог скачивания найден"):
                                    return True

                            return True

            raise AssertionError("PDF кнопка не найдена или не кликабельна")

    def download_mobile_pdf(self, project_name: str, file_type: str = "catalog"):
        """Скачать PDF файл на мобильном устройстве через полный флоу."""
        with allure.step(
            f"Скачиваем {file_type} PDF для {project_name.upper()} на мобильном устройстве"
        ):
            # Полный флоу навигации
            self.navigate_to_mobile_catalog_page(project_name)

            # Находим и кликаем на доступный apartment
            self.find_and_click_available_apartment()

            # Кликаем по PDF кнопке
            self.click_mobile_pdf_button()

            # Возвращаем имя файла
            return f"{project_name}_{file_type}_mobile.pdf"

    # ==================== МОБИЛЬНЫЕ ПРОВЕРКИ ====================

    def check_mobile_viewport_adaptation(self):
        """Проверить адаптивность на мобильном устройстве."""
        with allure.step("Проверяем адаптивность на мобильном устройстве"):
            viewport_width = self.page.viewport_size["width"]
            viewport_height = self.page.viewport_size["height"]

            # Проверяем размеры viewport
            assert (
                viewport_width <= 768
            ), f"Viewport слишком широкий для мобильного: {viewport_width}px"
            assert (
                viewport_height <= 1024
            ), f"Viewport слишком высокий для мобильного: {viewport_height}px"

            # Проверяем отсутствие горизонтальной прокрутки
            body_width = self.page.evaluate("document.body.scrollWidth")
            assert (
                body_width <= viewport_width
            ), "Страница требует горизонтальной прокрутки на мобильном"

            # Проверяем, что все важные элементы помещаются в viewport
            important_elements = self.page.locator("h1, h2, nav, .main-content").all()
            for element in important_elements:
                if element.is_visible():
                    bounding_box = element.bounding_box()
                    if bounding_box:
                        assert (
                            bounding_box["x"] + bounding_box["width"] <= viewport_width
                        ), f"Элемент выходит за границы viewport: {element}"

    def check_mobile_touch_elements(self):
        """Проверить, что элементы подходят для touch-интерфейса."""
        with allure.step("Проверяем элементы для touch-интерфейса"):
            # Проверяем размеры кнопок (должны быть не менее 44px для touch)
            buttons = self.page.locator('button, a, [role="button"]').all()
            for button in buttons:
                if button.is_visible():
                    bounding_box = button.bounding_box()
                    if bounding_box:
                        width = bounding_box["width"]
                        height = bounding_box["height"]
                        assert (
                            width >= 44 or height >= 44
                        ), f"Кнопка слишком мала для touch: {width}x{height}px - {button}"

    def check_mobile_modal_behavior(self):
        """Проверить поведение модальных окон на мобильных устройствах."""
        with allure.step("Проверяем поведение модальных окон на мобильном"):
            modals = self.page.locator(MOBILE_PROJECT_INFO_MODAL).all()
            for modal in modals:
                if modal.is_visible():
                    # Проверяем, что модальное окно занимает разумную часть экрана
                    bounding_box = modal.bounding_box()
                    if bounding_box:
                        viewport_width = self.page.viewport_size["width"]
                        modal_width = bounding_box["width"]

                        # Модальное окно должно занимать не менее 60% ширины экрана
                        assert (
                            modal_width >= viewport_width * 0.6
                        ), f"Модальное окно слишком узкое: {modal_width}px из {viewport_width}px"

    # ==================== УТИЛИТЫ ДЛЯ МОБИЛЬНЫХ ТЕСТОВ ====================

    def scroll_mobile_page(self, direction: str = "down", distance: int = 300):
        """Прокрутить страницу на мобильном устройстве."""
        if direction == "down":
            self.page.mouse.wheel(0, distance)
        elif direction == "up":
            self.page.mouse.wheel(0, -distance)
        elif direction == "left":
            self.page.mouse.wheel(-distance, 0)
        elif direction == "right":
            self.page.mouse.wheel(distance, 0)

        # Ждем завершения прокрутки
        self.page.wait_for_timeout(500)

    def simulate_mobile_swipe(self, start_x: int, start_y: int, end_x: int, end_y: int):
        """Симулировать свайп на мобильном устройстве."""
        # Начинаем touch действие
        self.page.touchscreen.tap(start_x, start_y)

        # Движемся к конечной точке
        self.page.mouse.move(end_x, end_y)

        # Завершаем touch действие
        self.page.mouse.up()

    # ==================== МЕТОДЫ НАВИГАЦИИ ПО ЗДАНИЯМ И ЭТАЖАМ ====================

    # ==================== МЕТОДЫ НАВИГАЦИИ - ДЕЛЕГАТЫ К MOBILE_NAVIGATION ====================

    def close_zoom_modal(self) -> bool:
        """Закрывает модальное окно 'Zoom and drag screen'."""
        return self.mobile_navigation.close_zoom_modal()

    def click_building(self, building_number: str) -> bool:
        """Кликает на здание."""
        return self.mobile_navigation.click_building(building_number)

    def click_view_building_button(self) -> bool:
        """Кликает на кнопку 'View' для здания."""
        return self.mobile_navigation.click_view_building_button()

    def click_floor(self, floor_number: str) -> bool:
        """Кликает на этаж."""
        return self.mobile_navigation.click_floor(floor_number)

    def click_view_floor_button(self) -> bool:
        """Кликает на кнопку 'View Floor'."""
        return self.mobile_navigation.click_view_floor_button()

    def click_apartment_on_plan(self) -> bool:
        """Кликает на квартиру на плане этажа."""
        return self.mobile_navigation.click_apartment_on_plan()

    def click_view_apartment_button(self) -> bool:
        """Кликает на кнопку 'View Apartment'."""
        return self.mobile_navigation.click_view_apartment_button()

    def click_view_3d_button(self) -> bool:
        """Кликает на кнопку 'View in 3D'."""
        view_3d_button = self.page.locator(
            '[data-test-id="info-content-primary-button"]'
        )

        if view_3d_button.count() > 1:
            view_3d_button.nth(1).click(force=True)
            self.page.wait_for_timeout(3000)
            return "/apartment/" in self.page.url
        return False

    def navigate_building_floor_apartment(
        self, building_number: str = "1", floor_number: str = "1"
    ) -> bool:
        """Полная навигация: здание -> этаж -> квартира."""
        return self.mobile_navigation.navigate_building_floor_apartment(
            building_number, floor_number
        )

    def check_building_navigation_success(self) -> bool:
        """Проверяет успешность навигации по зданию."""
        current_url = self.page.url
        return "/building/" in current_url
