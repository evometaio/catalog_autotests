"""Мобильный компонент для навигации по зданиям и этажам."""

import allure
from playwright.sync_api import Page

from locators.mobile_locators import (
    MOBILE_VIEW_BUTTON,
    MOBILE_MODAL_OK_BUTTON,
    MOBILE_APARTMENT_PATH,
    MOBILE_VIEW_APARTMENT_BUTTON,
    MOBILE_TIMEOUTS,
    MOBILE_APARTMENT_SELECTOR,
    MOBILE_APARTMENT_LOCK_ICON,
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
        self, 
        building_number: str = "1", 
        floor_number: str = "1"
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

