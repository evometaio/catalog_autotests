"""
Мобильная страница с методами, специфичными для мобильных устройств.
Содержит адаптивные локаторы и методы для работы с мобильным UI.
"""

import allure
from playwright.sync_api import Page, Locator
from .base_page import BasePage
from locators.mobile_locators import (
    MOBILE_PROJECT_SELECTORS,
    MOBILE_PROJECT_INFO_MODAL,
    MOBILE_MODAL_MASK,
    MOBILE_MODAL_CONTENT,
    MOBILE_EXPLORE_BUTTON,
    MOBILE_CLOSE_BUTTON,
    MOBILE_ARISHA_MENU_BUTTON,
    MOBILE_ALL_UNITS_BUTTON,
    MOBILE_PDF_BUTTON,
    MOBILE_APARTMENT_SELECTOR,
    MOBILE_APARTMENT_LOCK_ICON,
    MOBILE_NAVIGATION_MENU,
    MOBILE_NAVIGATION_LIST,
    MOBILE_MENU_ITEMS,
    MOBILE_VIEWPORT_CONTAINER,
    MOBILE_TOUCH_ELEMENTS,
    MOBILE_MODAL_DIALOG,
    MOBILE_FORM_INPUTS,
    MOBILE_FORM_BUTTONS,
    MOBILE_CONTENT_IMAGES,
    MOBILE_CONTENT_TEXT,
    MOBILE_CONTENT_LINKS,
    MOBILE_ERROR_MESSAGES,
    MOBILE_LOADING_INDICATORS,
    MOBILE_NOTIFICATION,
    MOBILE_TOAST_MESSAGE,
    MOBILE_LOADING_OVERLAY,
    MOBILE_SPINNER,
    MOBILE_SCROLLABLE_CONTAINER,
    MOBILE_SCROLL_INDICATOR,
    MOBILE_HORIZONTAL_MENU_ITEM,
    MOBILE_BUILDING_SELECTOR,
    MOBILE_FLOOR_SELECTOR,
    MOBILE_VIEW_BUTTON,
    MOBILE_MODAL_OK_BUTTON,
    MOBILE_APARTMENT_SVG,
    MOBILE_APARTMENT_PATH,
    MOBILE_APARTMENT_VISIBLE_CLASS,
    MOBILE_APARTMENT_RECT,
    MOBILE_APARTMENT_CIRCLE,
    get_mobile_project_selector,
    get_mobile_apartment_selector,
    get_mobile_button_selector,
    get_mobile_icon_selector,
    get_mobile_building_selector,
    get_mobile_floor_selector,
    MOBILE_TIMEOUTS
)


class MobilePage(BasePage):
    """Мобильная версия BasePage с адаптивными методами."""

    def __init__(self, page: Page):
        # Устанавливаем базовые URL-ы для разных окружений
        import os
        environment = os.getenv("TEST_ENVIRONMENT", "dev")
        if environment == "dev":
            base_url = os.getenv("DEV_AGENT_BASE_URL", "https://qube-dev-next.evometa.io/agent/map")
            self.agent_base_url = os.getenv("DEV_AGENT_BASE_URL", "https://qube-dev-next.evometa.io/agent/map")
            self.client_base_url = os.getenv("DEV_CLIENT_BASE_URL", "https://qube-dev-next.evometa.io/client/map")
        else:
            base_url = os.getenv("AGENT_PROD_BASE_URL", "https://virtualtours.qbd.ae/agent/map")
            self.agent_base_url = os.getenv("AGENT_PROD_BASE_URL", "https://virtualtours.qbd.ae/agent/map")
            self.client_base_url = os.getenv("CLIENT_PROD_BASE_URL", "https://virtualtours.qbd.ae/client/map")
        
        # Инициализируем BasePage с правильным URL
        super().__init__(page, base_url)
        self.device_type = "mobile"

    # ==================== МОБИЛЬНЫЕ ЛОКАТОРЫ ====================
    # Все локаторы теперь импортируются из locators/mobile_locators.py

    # ==================== МОБИЛЬНЫЕ МЕТОДЫ ДЛЯ КАРТЫ ====================

    def get_mobile_project_selector(self, project_name: str) -> str:
        """Получить мобильный селектор для проекта."""
        return get_mobile_project_selector(project_name)

    def click_mobile_project_on_map(self, project_name: str):
        """Кликнуть по проекту на карте для мобильных устройств."""
        with allure.step(f"Кликаем по проекту {project_name.upper()} на мобильном устройстве"):
            # Получаем мобильный селектор
            selector = self.get_mobile_project_selector(project_name)
            
            # Ждем появления проекта на карте
            project_element = self.page.locator(selector)
            project_element.wait_for(state="visible", timeout=10000)
            
            # Кликаем по проекту
            project_element.click()
            
            # Ждем появления мобильного модального окна
            self.wait_for_mobile_project_modal()

    def wait_for_mobile_project_modal(self):
        """Ждать появления мобильного модального окна с информацией о проекте."""
        mobile_modal = self.page.locator(MOBILE_PROJECT_INFO_MODAL)
        mobile_modal.wait_for(state="visible", timeout=10000)
        
        # Дополнительно проверяем, что модальное окно действительно видимо
        assert mobile_modal.is_visible(), "Мобильное модальное окно не видимо"

    def click_mobile_explore_project_button(self, project_name: str):
        """Кликнуть по кнопке Explore Project в мобильном модальном окне."""
        with allure.step(f"Кликаем на кнопку Explore Project для {project_name.upper()}"):
            # Ждем появления кнопки Explore Project
            explore_button = self.page.locator(MOBILE_EXPLORE_BUTTON)
            explore_button.wait_for(state="visible", timeout=10000)
            
            # Проверяем, что кнопка активна
            assert explore_button.is_enabled(), f"Кнопка Explore Project заблокирована для проекта {project_name}"
            
            # Кликаем по кнопке
            explore_button.click()
            
            # Ждем перехода на страницу проекта
            expected_url_pattern = f"**/{project_name.lower()}/**"
            self.page.wait_for_url(expected_url_pattern, timeout=10000)

    def close_mobile_project_modal(self):
        """Закрыть мобильное модальное окно."""
        # Пытаемся найти кнопку закрытия
        close_button = self.page.locator(MOBILE_CLOSE_BUTTON)
        
        if close_button.count() > 0 and close_button.is_visible():
            close_button.click()
        else:
            # Если нет кнопки закрытия, кликаем по маске
            mask = self.page.locator(MOBILE_MODAL_MASK)
            if mask.is_visible():
                mask.click()
            else:
                # Последний вариант - нажатие Escape
                self.page.keyboard.press("Escape")

    # ==================== МОБИЛЬНЫЕ МЕТОДЫ НАВИГАЦИИ ====================

    def navigate_to_mobile_project_from_map(self, project_name: str):
        """Полная навигация от карты до страницы проекта на мобильном устройстве."""
        with allure.step(f"Переходим от карты к проекту {project_name.upper()} на мобильном устройстве"):
            # Открываем карту
            self.open(route_type="map")
            
            # Кликаем по проекту
            self.click_mobile_project_on_map(project_name)
            
            # Кликаем по кнопке Explore Project
            self.click_mobile_explore_project_button(project_name)
            
            # Проверяем успешность перехода
            current_url = self.page.url
            assert f"/{project_name.lower()}/" in current_url, f"Не удалось перейти к проекту {project_name}"

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
                '[data-testid*="agent"]'
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
        with allure.step(f"Переходим на страницу каталога {project_name.upper()} через полную навигацию"):
            # 1. Переходим на карту агента
            self.page.goto(self.agent_base_url)
            self.page.wait_for_load_state("domcontentloaded")
            
            # 2. Кликаем по проекту на карте
            self.click_mobile_project_on_map(project_name)
            
            # 3. Кликаем на "Explore Project"
            self.click_mobile_explore_project_button(project_name)
            
            # 4. Кликаем на кнопку проекта (например, "arisha") для открытия меню
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
            else:
                # Для других проектов может потребоваться другая логика
                raise NotImplementedError(f"Навигация к каталогу для проекта {project_name} не реализована")

    # ==================== МОБИЛЬНЫЕ МЕТОДЫ ДЛЯ ФАЙЛОВ ====================

    def find_and_click_available_apartment(self):
        """Найти и кликнуть на первый доступный apartment."""
        with allure.step("Ищем свободный apartment"):
            self.page.wait_for_timeout(MOBILE_TIMEOUTS["apartment_load"])  # Ждем загрузки apartments
            
            # Ищем все apartments
            apartment_titles = self.page.locator(MOBILE_APARTMENT_SELECTOR)
            apartment_count = apartment_titles.count()
            
            if apartment_count == 0:
                raise AssertionError("Apartments не найдены")
            
            # Ищем первый доступный apartment (без замка)
            for i in range(apartment_count):
                apartment_title = apartment_titles.nth(i)
                
                if not apartment_title.is_visible():
                    continue
                
                # Проверяем, есть ли замок (элемент с иконкой замка)
                parent_card = apartment_title.locator('xpath=ancestor::div[contains(@class, "ant-card")]')
                lock_icons = parent_card.locator(MOBILE_APARTMENT_LOCK_ICON).count()
                
                if lock_icons == 0:  # Нет замка - apartment доступен
                    with allure.step(f"Кликаем на доступный apartment {i+1}"):
                        apartment_title.click()
                        self.page.wait_for_timeout(MOBILE_TIMEOUTS["medium"])
                        return True
            
            raise AssertionError("Доступные apartments не найдены")

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
                    parent_button = icon.locator('xpath=..').first
                    parent_tag = parent_button.evaluate('el => el.tagName')
                    
                    if parent_tag.lower() == 'button':
                        with allure.step(f"Кликаем на PDF кнопку {i+1}"):
                            parent_button.click()
                            self.page.wait_for_timeout(MOBILE_TIMEOUTS["medium"])
                            
                            # Проверяем, появился ли диалог скачивания
                            download_dialogs = self.page.locator('dialog, [role="dialog"]')
                            if download_dialogs.count() > 0:
                                with allure.step("Диалог скачивания найден"):
                                    return True
                            
                            return True
            
            raise AssertionError("PDF кнопка не найдена или не кликабельна")

    def download_mobile_pdf(self, project_name: str, file_type: str = "catalog"):
        """Скачать PDF файл на мобильном устройстве через полный флоу."""
        with allure.step(f"Скачиваем {file_type} PDF для {project_name.upper()} на мобильном устройстве"):
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
            viewport_width = self.page.viewport_size['width']
            viewport_height = self.page.viewport_size['height']
            
            # Проверяем размеры viewport
            assert viewport_width <= 768, f"Viewport слишком широкий для мобильного: {viewport_width}px"
            assert viewport_height <= 1024, f"Viewport слишком высокий для мобильного: {viewport_height}px"
            
            # Проверяем отсутствие горизонтальной прокрутки
            body_width = self.page.evaluate("document.body.scrollWidth")
            assert body_width <= viewport_width, "Страница требует горизонтальной прокрутки на мобильном"
            
            # Проверяем, что все важные элементы помещаются в viewport
            important_elements = self.page.locator('h1, h2, nav, .main-content').all()
            for element in important_elements:
                if element.is_visible():
                    bounding_box = element.bounding_box()
                    if bounding_box:
                        assert bounding_box['x'] + bounding_box['width'] <= viewport_width, \
                            f"Элемент выходит за границы viewport: {element}"

    def check_mobile_touch_elements(self):
        """Проверить, что элементы подходят для touch-интерфейса."""
        with allure.step("Проверяем элементы для touch-интерфейса"):
            # Проверяем размеры кнопок (должны быть не менее 44px для touch)
            buttons = self.page.locator('button, a, [role="button"]').all()
            for button in buttons:
                if button.is_visible():
                    bounding_box = button.bounding_box()
                    if bounding_box:
                        width = bounding_box['width']
                        height = bounding_box['height']
                        assert width >= 44 or height >= 44, \
                            f"Кнопка слишком мала для touch: {width}x{height}px - {button}"

    def check_mobile_modal_behavior(self):
        """Проверить поведение модальных окон на мобильных устройствах."""
        with allure.step("Проверяем поведение модальных окон на мобильном"):
            modals = self.page.locator(MOBILE_PROJECT_INFO_MODAL).all()
            for modal in modals:
                if modal.is_visible():
                    # Проверяем, что модальное окно занимает разумную часть экрана
                    bounding_box = modal.bounding_box()
                    if bounding_box:
                        viewport_width = self.page.viewport_size['width']
                        modal_width = bounding_box['width']
                        
                        # Модальное окно должно занимать не менее 60% ширины экрана
                        assert modal_width >= viewport_width * 0.6, \
                            f"Модальное окно слишком узкое: {modal_width}px из {viewport_width}px"

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

    def close_zoom_modal(self) -> bool:
        """Закрывает модальное окно 'Zoom and drag screen'."""
        try:
            ok_button = self.page.locator(MOBILE_MODAL_OK_BUTTON)
            if ok_button.is_visible():
                ok_button.click()
                self.page.wait_for_timeout(MOBILE_TIMEOUTS["short"])
                allure.attach(
                    "Модальное окно 'Zoom and drag screen' закрыто",
                    name="Zoom Modal Closed",
                    attachment_type=allure.attachment_type.TEXT
                )
                return True
            return False
        except Exception as e:
            allure.attach(
                f"Ошибка при закрытии модального окна: {str(e)}",
                name="Zoom Modal Error",
                attachment_type=allure.attachment_type.TEXT
            )
            return False

    def click_building(self, building_number: str) -> bool:
        """Кликает на здание по номеру."""
        try:
            building_selector = get_mobile_building_selector(building_number)
            building_element = self.page.locator(building_selector)
            
            if building_element.is_visible():
                building_element.click()
                self.page.wait_for_timeout(MOBILE_TIMEOUTS["short"])
                allure.attach(
                    f"Клик по зданию '{building_number}' выполнен",
                    name="Building Click",
                    attachment_type=allure.attachment_type.TEXT
                )
                return True
            else:
                allure.attach(
                    f"Здание '{building_number}' не найдено",
                    name="Building Not Found",
                    attachment_type=allure.attachment_type.TEXT
                )
                return False
        except Exception as e:
            allure.attach(
                f"Ошибка при клике на здание: {str(e)}",
                name="Building Click Error",
                attachment_type=allure.attachment_type.TEXT
            )
            return False

    def click_view_building_button(self) -> bool:
        """Кликает на кнопку 'View' для здания."""
        try:
            view_button = self.page.locator(MOBILE_VIEW_BUTTON)
            if view_button.is_visible():
                view_button.click(force=True)
                self.page.wait_for_timeout(MOBILE_TIMEOUTS["medium"])
                allure.attach(
                    "Клик по кнопке 'View Building' выполнен",
                    name="View Building Click",
                    attachment_type=allure.attachment_type.TEXT
                )
                return True
            else:
                allure.attach(
                    "Кнопка 'View Building' не найдена",
                    name="View Building Not Found",
                    attachment_type=allure.attachment_type.TEXT
                )
                return False
        except Exception as e:
            allure.attach(
                f"Ошибка при клике на кнопку 'View Building': {str(e)}",
                name="View Building Error",
                attachment_type=allure.attachment_type.TEXT
            )
            return False

    def click_floor(self, floor_number: str) -> bool:
        """Кликает на этаж по номеру."""
        try:
            floor_selector = get_mobile_floor_selector(floor_number)
            floor_element = self.page.locator(floor_selector)
            
            if floor_element.is_visible():
                floor_element.click()
                self.page.wait_for_timeout(MOBILE_TIMEOUTS["short"])
                allure.attach(
                    f"Клик по этажу '{floor_number}' выполнен",
                    name="Floor Click",
                    attachment_type=allure.attachment_type.TEXT
                )
                return True
            else:
                allure.attach(
                    f"Этаж '{floor_number}' не найден",
                    name="Floor Not Found",
                    attachment_type=allure.attachment_type.TEXT
                )
                return False
        except Exception as e:
            allure.attach(
                f"Ошибка при клике на этаж: {str(e)}",
                name="Floor Click Error",
                attachment_type=allure.attachment_type.TEXT
            )
            return False

    def click_view_floor_button(self) -> bool:
        """Кликает на кнопку 'View Floor'."""
        try:
            view_button = self.page.locator(MOBILE_VIEW_BUTTON)
            if view_button.is_visible():
                view_button.click(force=True)
                self.page.wait_for_timeout(MOBILE_TIMEOUTS["medium"])
                allure.attach(
                    "Клик по кнопке 'View Floor' выполнен",
                    name="View Floor Click",
                    attachment_type=allure.attachment_type.TEXT
                )
                return True
            else:
                allure.attach(
                    "Кнопка 'View Floor' не найдена",
                    name="View Floor Not Found",
                    attachment_type=allure.attachment_type.TEXT
                )
                return False
        except Exception as e:
            allure.attach(
                f"Ошибка при клике на кнопку 'View Floor': {str(e)}",
                name="View Floor Error",
                attachment_type=allure.attachment_type.TEXT
            )
            return False

    def click_apartment_on_plan(self) -> bool:
        """Кликает на квартиру на плане этажа."""
        try:
            apartment_paths = self.page.locator(MOBILE_APARTMENT_PATH)
            apartment_count = apartment_paths.count()
            
            if apartment_count > 0:
                # Ищем первую видимую квартиру
                for i in range(apartment_count):
                    apartment = apartment_paths.nth(i)
                    if apartment.is_visible():
                        apartment.click()
                        self.page.wait_for_timeout(MOBILE_TIMEOUTS["apartment_load"])
                        allure.attach(
                            f"Клик по квартире выполнен (найдено {apartment_count} квартир)",
                            name="Apartment Click",
                            attachment_type=allure.attachment_type.TEXT
                        )
                        return True
                
                allure.attach(
                    "Видимые квартиры не найдены",
                    name="Apartment Not Visible",
                    attachment_type=allure.attachment_type.TEXT
                )
                return False
            else:
                allure.attach(
                    "Квартиры не найдены",
                    name="No Apartments Found",
                    attachment_type=allure.attachment_type.TEXT
                )
                return False
        except Exception as e:
            allure.attach(
                f"Ошибка при клике на квартиру: {str(e)}",
                name="Apartment Click Error",
                attachment_type=allure.attachment_type.TEXT
            )
            return False

    def navigate_building_floor_apartment(self, building_number: str = "1", floor_number: str = "1") -> bool:
        """Полная навигация: здание -> этаж -> квартира."""
        try:
            # 1. Закрываем модальное окно если есть
            self.close_zoom_modal()
            
            # 2. Кликаем на здание
            if not self.click_building(building_number):
                return False
            
            # 3. Кликаем на кнопку "View Building"
            if not self.click_view_building_button():
                return False
            
            # 4. Кликаем на этаж
            if not self.click_floor(floor_number):
                return False
            
            # 5. Кликаем на кнопку "View Floor"
            if not self.click_view_floor_button():
                return False
            
            # 6. Кликаем на квартиру
            if not self.click_apartment_on_plan():
                return False
            
            allure.attach(
                f"Навигация завершена: здание {building_number} -> этаж {floor_number} -> квартира",
                name="Navigation Complete",
                attachment_type=allure.attachment_type.TEXT
            )
            return True
            
        except Exception as e:
            allure.attach(
                f"Ошибка при навигации: {str(e)}",
                name="Navigation Error",
                attachment_type=allure.attachment_type.TEXT
            )
            return False

    def check_building_navigation_success(self) -> bool:
        """Проверяет успешность навигации по зданию."""
        try:
            current_url = self.page.url
            if '/building/' in current_url:
                allure.attach(
                    f"Навигация успешна. URL: {current_url}",
                    name="Navigation Success",
                    attachment_type=allure.attachment_type.TEXT
                )
                return True
            else:
                allure.attach(
                    f"Навигация не завершена. URL: {current_url}",
                    name="Navigation Incomplete",
                    attachment_type=allure.attachment_type.TEXT
                )
                return False
        except Exception as e:
            allure.attach(
                f"Ошибка при проверке навигации: {str(e)}",
                name="Navigation Check Error",
                attachment_type=allure.attachment_type.TEXT
            )
            return False
