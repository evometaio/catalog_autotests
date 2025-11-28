"""Мобильный компонент для навигации по зданиям и этажам."""

import allure
from playwright.sync_api import Page

from locators.mobile_locators import (
    MOBILE_APARTMENT_LOCK_ICON,
    MOBILE_APARTMENT_PATH,
    MOBILE_APARTMENT_SELECTOR,
    MOBILE_MODAL_OK_BUTTON,
    MOBILE_TIMEOUTS,
    MOBILE_VIEW_APARTMENT_BUTTON,
    MOBILE_VIEW_BUTTON,
    get_mobile_building_selector,
)


class MobileNavigationComponent:
    """
    Мобильный компонент навигации.

    Ответственность:
    - Навигация по зданиям на мобильных
    - Навигация по этажам на мобильных
    - Навигация по апартаментам на мобильных
    """

    def __init__(self, page: Page):
        """
        Инициализация мобильного компонента навигации.

        Args:
            page: Playwright Page объект
        """
        self.page = page

    def close_zoom_modal(self) -> bool:
        """Закрывает модальное окно 'Zoom and drag screen'."""
        try:
            ok_button = self.page.locator(MOBILE_MODAL_OK_BUTTON)

            try:
                ok_button.wait_for(state="visible", timeout=5000)
                ok_button.click()
                ok_button.wait_for(state="hidden", timeout=5000)

                allure.attach(
                    "Модальное окно 'Zoom and drag screen' закрыто",
                    name="Zoom Modal Closed",
                    attachment_type=allure.attachment_type.TEXT,
                )
                return True
            except:
                allure.attach(
                    "Модальное окно не найдено (возможно, уже закрыто)",
                    name="Zoom Modal Not Found",
                    attachment_type=allure.attachment_type.TEXT,
                )
                return True

        except Exception as e:
            allure.attach(
                f"Ошибка при закрытии модального окна: {str(e)}",
                name="Zoom Modal Error",
                attachment_type=allure.attachment_type.TEXT,
            )
            return False

    def click_building(self, building_number: str) -> bool:
        """
        Кликает на здание по номеру (SVG path).

        Args:
            building_number: Номер здания

        Returns:
            bool: True если клик успешен
        """
        try:
            building_selector = get_mobile_building_selector(building_number)
            building_element = self.page.locator(building_selector)

            building_element.wait_for(state="visible", timeout=10000)
            building_element.click(force=True)

            # Ждем появления кнопки "View"
            self.page.locator(MOBILE_VIEW_BUTTON).wait_for(
                state="visible", timeout=5000
            )

            allure.attach(
                f"Клик по зданию '{building_number}' выполнен",
                name="Building Click",
                attachment_type=allure.attachment_type.TEXT,
            )
            return True

        except Exception as e:
            allure.attach(
                f"Ошибка при клике на здание: {str(e)}",
                name="Building Click Error",
                attachment_type=allure.attachment_type.TEXT,
            )
            return False

    def click_view_building_button(self) -> bool:
        """Кликает на кнопку 'View' для здания."""
        try:
            view_button = self.page.locator(MOBILE_VIEW_BUTTON)

            if view_button.is_visible():
                view_button.click(force=True)
                allure.attach(
                    "Клик по кнопке 'View Building' выполнен",
                    name="View Building Click",
                    attachment_type=allure.attachment_type.TEXT,
                )
                return True
            else:
                return False

        except Exception as e:
            allure.attach(
                f"Ошибка при клике на кнопку 'View Building': {str(e)}",
                name="View Building Error",
                attachment_type=allure.attachment_type.TEXT,
            )
            return False

    def click_floor(self, floor_number: str) -> bool:
        """
        Кликает на этаж по номеру.

        Args:
            floor_number: Номер этажа

        Returns:
            bool: True если клик успешен
        """
        try:
            floor_containers = self.page.locator(
                ".react-horizontal-scrolling-menu--item"
            )
            floor_container_count = floor_containers.count()

            for i in range(floor_container_count):
                try:
                    floor_element = floor_containers.nth(i)
                    floor_text = floor_element.text_content()

                    if floor_text.strip() == floor_number:
                        floor_element.click(force=True)
                        self.page.wait_for_timeout(500)

                        # Проверяем появление кнопки "View floor"
                        view_floor_button = self.page.locator(
                            'button:has-text("View floor")'
                        )
                        if view_floor_button.is_visible():
                            allure.attach(
                                f"Кнопка 'View floor' найдена после клика по этажу {floor_number}",
                                name="View Floor Found",
                                attachment_type=allure.attachment_type.TEXT,
                            )
                            return True
                except Exception:
                    continue

            return False

        except Exception as e:
            allure.attach(
                f"Ошибка при клике на этаж: {str(e)}",
                name="Floor Click Error",
                attachment_type=allure.attachment_type.TEXT,
            )
            return False

    def click_view_floor_button(self) -> bool:
        """Кликает на кнопку 'View Floor'."""
        try:
            view_floor_button = self.page.locator('button:has-text("View floor")')

            if view_floor_button.is_visible():
                view_floor_button.click(force=True)
                allure.attach(
                    "Клик по кнопке 'View Floor' выполнен",
                    name="View Floor Click",
                    attachment_type=allure.attachment_type.TEXT,
                )
                return True
            else:
                return False

        except Exception as e:
            allure.attach(
                f"Ошибка при клике на кнопку 'View Floor': {str(e)}",
                name="View Floor Error",
                attachment_type=allure.attachment_type.TEXT,
            )
            return False

    def click_apartment_on_plan(self) -> bool:
        """Кликает на квартиру на плане этажа."""
        try:
            apartment_paths = self.page.locator(MOBILE_APARTMENT_PATH)
            apartment_count = apartment_paths.count()

            allure.attach(
                f"Найдено квартир: {apartment_count}",
                name="Apartment Count",
                attachment_type=allure.attachment_type.TEXT,
            )

            if apartment_count > 0:
                for i in range(apartment_count):
                    apartment = apartment_paths.nth(i)
                    if apartment.is_visible():
                        apartment.click()
                        allure.attach(
                            f"Клик по квартире выполнен",
                            name="Apartment Click",
                            attachment_type=allure.attachment_type.TEXT,
                        )
                        return True
                return False
            else:
                return False

        except Exception as e:
            allure.attach(
                f"Ошибка при клике на квартиру: {str(e)}",
                name="Apartment Click Error",
                attachment_type=allure.attachment_type.TEXT,
            )
            return False

    def click_view_apartment_button(self) -> bool:
        """Кликает на кнопку 'View Apartment' после выбора квартиры."""
        try:
            view_apartment_button = self.page.locator(MOBILE_VIEW_APARTMENT_BUTTON)

            if view_apartment_button.is_visible():
                view_apartment_button.click(force=True)
                allure.attach(
                    "Клик по кнопке 'View Apartment' выполнен",
                    name="View Apartment Click",
                    attachment_type=allure.attachment_type.TEXT,
                )
                return True
            else:
                return False

        except Exception as e:
            allure.attach(
                f"Ошибка при клике на кнопку 'View Apartment': {str(e)}",
                name="View Apartment Error",
                attachment_type=allure.attachment_type.TEXT,
            )
            return False

    def navigate_building_floor_apartment(
        self, building_number: str = "1", floor_number: str = "1"
    ) -> bool:
        """
        Полная навигация: здание -> этаж -> квартира.

        Args:
            building_number: Номер здания
            floor_number: Номер этажа

        Returns:
            bool: True если навигация успешна
        """
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
                attachment_type=allure.attachment_type.TEXT,
            )
            return True

        except Exception as e:
            allure.attach(
                f"Ошибка при навигации: {str(e)}",
                name="Navigation Error",
                attachment_type=allure.attachment_type.TEXT,
            )
            return False

    def open_mobile_menu(self) -> bool:
        """Открыть мобильное меню."""
        try:
            menu_toggle = self.page.locator('[data-test-id="nav-mobile-menu-toggle"]')
            menu_toggle.wait_for(state="visible", timeout=10000)
            menu_toggle.click()
            self.page.wait_for_timeout(1000)
            return True
        except Exception as e:
            allure.attach(
                f"Ошибка при открытии мобильного меню: {str(e)}",
                name="Mobile Menu Error",
                attachment_type=allure.attachment_type.TEXT,
            )
            return False

    def click_mark_building_menu(self) -> bool:
        """Кликнуть на 'Корпус' в мобильном меню для mark."""
        try:
            building_menu = self.page.locator('[data-test-id="nav-mobile-building"]')
            building_menu.wait_for(state="visible", timeout=5000)
            building_menu.click()
            self.page.wait_for_timeout(1000)
            return True
        except Exception as e:
            allure.attach(
                f"Ошибка при клике на меню корпуса: {str(e)}",
                name="Building Menu Error",
                attachment_type=allure.attachment_type.TEXT,
            )
            return False

    def click_mark_building_item(self, building_number: int = 1) -> bool:
        """Кликнуть на корпус в списке для mark."""
        try:
            building_item = self.page.locator(
                f'[data-test-id="nav-mobile-building-item-mark-k{building_number}"]'
            )
            building_item.wait_for(state="visible", timeout=5000)
            building_item.click()
            self.page.wait_for_timeout(2000)

            # Проверяем переход
            self.page.wait_for_url(
                f"**/building/mark-k{building_number}", timeout=10000
            )
            return True
        except Exception as e:
            allure.attach(
                f"Ошибка при клике на корпус: {str(e)}",
                name="Building Item Error",
                attachment_type=allure.attachment_type.TEXT,
            )
            return False

    def click_mark_floor_item(self, floor_number: int) -> bool:
        """Кликнуть на этаж внизу страницы для mark."""
        try:
            floor_item = self.page.locator(
                f'xpath=//div[contains(@class, "_itemInner_17qm7_18") and text()="{floor_number}"]'
            )
            floor_item.wait_for(state="visible", timeout=10000)
            floor_item.first.click()
            self.page.wait_for_timeout(1000)
            return True
        except Exception as e:
            allure.attach(
                f"Ошибка при клике на этаж: {str(e)}",
                name="Floor Item Error",
                attachment_type=allure.attachment_type.TEXT,
            )
            return False

    def click_mark_view_floor_button(self, floor_number: int) -> bool:
        """Кликнуть на кнопку 'Посмотреть этаж' для mark."""
        try:
            view_floor_button = self.page.locator(
                f'button:has-text("Посмотреть этаж {floor_number}")'
            )
            view_floor_button.wait_for(state="visible", timeout=5000)
            view_floor_button.click()
            self.page.wait_for_timeout(2000)
            return True
        except Exception as e:
            allure.attach(
                f"Ошибка при клике на кнопку 'Посмотреть этаж': {str(e)}",
                name="View Floor Button Error",
                attachment_type=allure.attachment_type.TEXT,
            )
            return False

    def click_mark_apartment_item(self) -> str:
        """Кликнуть на первый доступный апартамент внизу страницы для mark. Возвращает номер апартамента."""
        try:
            apartment_items = self.page.locator("div._itemInner_17qm7_18")
            first_apartment = apartment_items.first
            first_apartment.wait_for(state="visible", timeout=10000)

            apartment_number = first_apartment.text_content()
            first_apartment.click()
            self.page.wait_for_timeout(2000)

            return apartment_number
        except Exception as e:
            allure.attach(
                f"Ошибка при клике на апартамент: {str(e)}",
                name="Apartment Item Error",
                attachment_type=allure.attachment_type.TEXT,
            )
            return ""

    def click_mark_view_apartment_button(self, apartment_number: str) -> bool:
        """Кликнуть на кнопку 'Посмотреть квартиру' для mark."""
        try:
            view_apartment_button = self.page.locator(
                f'button:has-text("Посмотреть квартиру {apartment_number}")'
            )
            view_apartment_button.wait_for(state="visible", timeout=10000)

            # Скроллим к кнопке, чтобы она была видна
            view_apartment_button.scroll_into_view_if_needed()
            self.page.wait_for_timeout(500)

            view_apartment_button.click()
            self.page.wait_for_timeout(3000)
            return True
        except Exception as e:
            allure.attach(
                f"Ошибка при клике на кнопку 'Посмотреть квартиру': {str(e)}",
                name="View Apartment Button Error",
                attachment_type=allure.attachment_type.TEXT,
            )
            return False

    def click_mark_view_3d_button(self) -> bool:
        """Кликнуть на кнопку 'Посмотреть 3D Тур' для mark."""
        try:
            view_3d_button = self.page.get_by_role("button", name="Посмотреть 3D Тур")
            view_3d_button.wait_for(state="visible", timeout=10000)
            view_3d_button.first.click()
            self.page.wait_for_timeout(3000)
            return True
        except Exception as e:
            allure.attach(
                f"Ошибка при клике на кнопку 'Посмотреть 3D Тур': {str(e)}",
                name="View 3D Button Error",
                attachment_type=allure.attachment_type.TEXT,
            )
            return False

    def find_and_click_available_apartment(self):
        """Найти и кликнуть на первый доступный apartment в каталоге."""
        with allure.step("Ищем свободный apartment"):
            self.page.wait_for_timeout(MOBILE_TIMEOUTS["apartment_load"])

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

                # Проверяем замок
                parent_card = apartment_title.locator(
                    'xpath=ancestor::div[contains(@class, "ant-card")]'
                )
                lock_icons = parent_card.locator(MOBILE_APARTMENT_LOCK_ICON).count()

                if lock_icons == 0:
                    with allure.step(f"Кликаем на доступный apartment {i+1}"):
                        apartment_title.click()
                        self.page.wait_for_timeout(MOBILE_TIMEOUTS["medium"])
                        return True

            raise AssertionError("Доступные apartments не найдены")
