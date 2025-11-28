"""Страница проекта MARK (LSR)."""

from playwright.sync_api import Page

from locators.lsr.mark_locators import MarkLocators
from pages.base_page import BasePage
from pages.components.amenities_component import AmenitiesComponent
from pages.components.apartment_widget_component import ApartmentWidgetComponent
from pages.components.area_tour_360_component import AreaTour360Component
from pages.components.navigation_component import NavigationComponent


class MarkPage(BasePage):
    """
    Страница проекта MARK.

    Наследует от BasePage и добавляет специфичную функциональность MARK.
    Особенность: нет /map роута, только /area, нет agent и client routes.
    """

    def __init__(self, page: Page, url: str = None):
        """
        Инициализация MARK страницы.

        Args:
            page: Playwright Page объект
            url: URL страницы
        """
        if url is None:
            from conftest import _get_urls_by_environment

            urls = _get_urls_by_environment()
            url = urls["lsr_mark"]

        super().__init__(page, url, MarkLocators)

        # Переопределяем компоненты с правильными локаторами
        # MapComponent не нужен, так как нет карты
        self.amenities = AmenitiesComponent(page, self.project_locators)
        self.area_tour_360 = AreaTour360Component(page, self.project_locators)
        self.navigation = NavigationComponent(page, self.project_locators)
        self.apartment_widget = ApartmentWidgetComponent(page, MarkLocators, "mark")

        # Устанавливаем название проекта
        self.project_name = "mark"

    def click_all_units_button(self):
        """Кликнуть на кнопку Все квартиры (переход в каталог)."""
        self.browser.click(self.project_locators.NAV_DESKTOP_CATALOG2D_STANDALONE)
        self.page.wait_for_url("**/catalog_2d", timeout=10000)

    def click_contact_button(self):
        """Кликнуть на кнопку Оставить заявку."""
        self.browser.click(self.project_locators.CONTACT_BUTTON)

    def click_360_panorama_menu_item(self, menu_item: str = "yard"):
        """
        Кликнуть на пункт меню панорам.

        Args:
            menu_item: Тип панорамы - "rotation", "yard", "lobby-k1", "lobby-k2", "lobby-k3"
        """
        menu_selectors = {
            "rotation": self.project_locators.AREA_TOUR_360_MENU_ROTATION,
            "yard": self.project_locators.AREA_TOUR_360_MENU_TOUR_YARD,
            "lobby-k1": self.project_locators.AREA_TOUR_360_MENU_TOUR_LOBBY_K1,
            "lobby-k2": self.project_locators.AREA_TOUR_360_MENU_TOUR_LOBBY_K2,
            "lobby-k3": self.project_locators.AREA_TOUR_360_MENU_TOUR_LOBBY_K3,
        }

        selector = menu_selectors.get(menu_item)
        if not selector:
            raise ValueError(f"Неизвестный пункт меню: {menu_item}")

        self.browser.click(selector)

    def open(self, path: str = "", route_type: str = None):
        """
        Открыть страницу MARK.

        Args:
            path: Дополнительный путь к базовому URL
            route_type: Игнорируется для MARK (нет agent/client routes)
        """
        # Для MARK игнорируем route_type, так как нет agent/client routes
        url = self.base_url

        # Добавляем дополнительный путь если есть
        if path:
            url = f"{url.rstrip('/')}/{path.lstrip('/')}"

        self.page.goto(url)
        self.wait_for_page_load()

        # Принудительно сбрасываем масштаб страницы
        self.page.evaluate("document.body.style.zoom = '1'")
        self.page.evaluate("document.documentElement.style.zoom = '1'")

    def download_pdf_and_verify(self):
        """
        Скачать и проверить PDF для mark.

        Процесс:
        1. Кликаем на первую кнопку "Скачать PDF" в виджете апартамента
        2. Ждем появления модального окна
        3. Ждем загрузки PDF в модалке
        4. Кликаем на вторую кнопку "Скачать PDF" в модалке
        5. Скачиваем файл
        """
        import os
        import time

        import allure

        with allure.step("Кликаем на первую кнопку Скачать PDF в виджете"):
            # На мобильных устройствах сначала нужно открыть дополнительное меню
            mobile_info_button = self.page.locator(
                self.project_locators.MOBILE_INFO_MENU_BUTTON
            )
            is_mobile = (
                mobile_info_button.count() > 0 and mobile_info_button.first.is_visible()
            )

            if is_mobile:
                with allure.step("Открываем дополнительное меню на мобильном"):
                    mobile_info_button.first.click()
                # Для мобильной версии используем специфичный локатор из mark_locators
                pdf_button = self.page.locator(
                    self.project_locators.DOWNLOAD_PDF_BUTTON_MOBILE
                )
            else:
                # Для desktop используем обычный локатор
                pdf_button = self.page.locator(
                    self.project_locators.DOWNLOAD_PDF_BUTTON
                )

            pdf_button.wait_for(state="visible", timeout=10000)
            pdf_button.click()

        with allure.step("Ждем, пока кнопка Скачать PDF в модалке станет активной"):
            # Используем уникальный класс для поиска кнопки в модалке
            modal_pdf_button = self.page.locator(
                self.project_locators.DOWNLOAD_PDF_MODAL_BUTTON
            )
            # Ждем, пока кнопка станет видимой
            modal_pdf_button.wait_for(state="visible", timeout=30000)
            # Ждем, пока кнопка станет активной (исчезнет класс загрузки _loading_1atog_20)
            self.page.wait_for_function(
                """
                () => {
                    const button = document.querySelector('button.page_modalSalesOfferButton__Jw6OU');
                    return button && button.offsetParent !== null && !button.classList.contains('_loading_1atog_20');
                }
                """,
                timeout=60000,
            )

        with allure.step("Кликаем на кнопку Скачать PDF в модалке"):
            with self.page.expect_download(timeout=60000) as download_info:
                modal_pdf_button.click()

                download = download_info.value
                file_path = os.path.join("downloads", download.suggested_filename)
                os.makedirs("downloads", exist_ok=True)
                download.save_as(file_path)

        allure.attach(
            f"Файл сохранен: {file_path}",
            name="Download Info",
            attachment_type=allure.attachment_type.TEXT,
        )

        # Проверяем что файл существует
        success = os.path.exists(file_path) and os.path.getsize(file_path) > 0
        return success, file_path

    def cleanup_pdf_after_test(self):
        """Удалить скачанные PDF файлы после теста."""
        import os
        import shutil

        if os.path.exists("downloads"):
            shutil.rmtree("downloads")
            print("Удалены скачанные файлы")

    def click_mobile_pdf_button(self):
        """Кликнуть по PDF кнопке на мобильном устройстве для mark."""
        import allure

        with allure.step("Ищем и кликаем по PDF кнопке"):
            # Для mark используем специфичный локатор
            pdf_button = self.page.locator(self.project_locators.DOWNLOAD_PDF_BUTTON)
            pdf_button.wait_for(state="visible", timeout=10000)
            pdf_button.click()
            self.page.wait_for_timeout(1000)
            return True

    def check_mobile_viewport_adaptation(self):
        """Проверка адаптивности на мобильном устройстве."""
        # Базовая проверка - просто проверяем, что страница загружена
        self.page.wait_for_load_state("domcontentloaded")

    def navigate_to_building(self, building_number: int):
        """
        Перейти к зданию для MARK.

        Для MARK используется формат локатора: nav-desktop-building-mark-k{building_number}
        """
        import allure

        with allure.step(f"Переходим к зданию {building_number}"):
            # Кликаем на навигацию по зданиям
            building_nav = self.page.locator(self.project_locators.BUILDING_NAV_BUTTON)
            building_nav.click()

            # Для MARK используется формат: nav-desktop-building-mark-k1, nav-desktop-building-mark-k2 и т.д.
            building_button = (
                f'[data-test-id="nav-desktop-building-mark-k{building_number}"]'
            )

            # Ждем появления и стабилизации дропдауна
            self.page.wait_for_selector(building_button, state="visible", timeout=5000)
            self.page.wait_for_timeout(500)  # Ждем завершения анимации

            button = self.page.locator(building_button)
            button.click()

            # Ждем изменения URL (для MARK формат: /building/mark-k1, /building/mark-k2 и т.д.)
            self.page.wait_for_url(
                f"**/building/mark-k{building_number}", timeout=10000
            )

    def navigate_to_floor(self, floor_number: int):
        """
        Перейти к этажу для MARK.

        Для MARK используется xpath локатор: //li[@data-test-id="nav-desktop-floor-{floor_number}"]
        """
        import allure

        with allure.step(f"Переходим к этажу {floor_number}"):
            # Кликаем на навигацию по этажам
            floor_nav = self.page.locator(self.project_locators.FLOOR_NAV_BUTTON)
            floor_nav.click()

            # Для MARK используется xpath формат: //li[@data-test-id="nav-desktop-floor-{floor_number}"]
            floor_button = f'//li[@data-test-id="nav-desktop-floor-{floor_number}"]'

            # Ждем появления и стабилизации дропдауна
            self.page.wait_for_selector(floor_button, state="visible", timeout=5000)
            self.page.wait_for_timeout(500)  # Ждем завершения анимации

            button = self.page.locator(floor_button)
            button.click()

            # Ждем изменения URL (для MARK формат: /floor/mark-k1/1, /floor/mark-k1/2 и т.д.)
            # Нужно получить номер здания из текущего URL
            current_url = self.page.url
            building_part = "k1"  # По умолчанию k1, если не удалось определить
            if "/building/mark-k" in current_url:
                building_part = current_url.split("/building/mark-")[1].split("/")[0]

            self.page.wait_for_url(
                f"**/floor/mark-{building_part}/{floor_number}", timeout=10000
            )
