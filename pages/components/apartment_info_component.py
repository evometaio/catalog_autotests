"""Компонент для работы с информацией об апартаменте."""

import allure
from playwright.sync_api import Page


class ApartmentInfoComponent:
    """
    Компонент информации об апартаменте.
    
    Ответственность:
    - Проверка информации об апартаменте
    - Получение данных апартамента
    - Проверка особенностей апартамента
    """

    def __init__(self, page: Page, project_locators, project_name: str = "arisha"):
        """
        Инициализация компонента информации.
        
        Args:
            page: Playwright Page объект
            project_locators: Локаторы проекта
            project_name: Название проекта (для получения специфичных локаторов)
        """
        self.page = page
        self.project_name = project_name
        
        # Получаем локаторы информации для конкретного проекта
        # project_locators это КЛАСС локаторов (например, ArishaLocators)
        if hasattr(project_locators, 'ApartmentInfo'):
            self.locators = project_locators.ApartmentInfo
        else:
            self.locators = None

    def wait_for_info_to_appear(self):
        """Дождаться появления информации об апартаменте."""
        if not self.locators:
            raise ValueError(f"Локаторы информации не найдены для проекта {self.project_name}")
        
        with allure.step("Ожидаем появления информации об апартаменте"):
            self.page.wait_for_selector(
                self.locators.INFO_CONTAINER, 
                timeout=10000
            )

    def check_apartment_number(self, apartment_number: str = "104") -> bool:
        """
        Проверить номер апартамента.
        
        Args:
            apartment_number: Ожидаемый номер апартамента
            
        Returns:
            bool: True если номер корректный
        """
        if not self.locators:
            return False
        
        with allure.step(f"Проверяем номер апартамента: {apartment_number}"):
            apartment_element = self.page.locator(
                self.locators.APARTMENT_NUMBER
            ).first
            apartment_text = apartment_element.text_content()
            return f"APT. {apartment_number}" in apartment_text

    def check_apartment_type(self) -> bool:
        """
        Проверить тип апартамента.
        
        Returns:
            bool: True если тип отображается
        """
        if not self.locators:
            return False
        
        with allure.step("Проверяем тип апартамента"):
            type_element = self.page.locator(self.locators.TYPE_VALUE).first
            return type_element.is_visible()

    def check_floor_info(self) -> bool:
        """
        Проверить информацию о этаже.
        
        Returns:
            bool: True если информация о этаже отображается
        """
        if not self.locators:
            return False
        
        with allure.step("Проверяем информацию о этаже"):
            floor_element = self.page.locator(self.locators.FLOOR_VALUE).first
            return floor_element.is_visible()

    def check_building_info(self) -> bool:
        """
        Проверить информацию о здании.
        
        Returns:
            bool: True если информация о здании отображается
        """
        if not self.locators:
            return False
        
        with allure.step("Проверяем информацию о здании"):
            building_element = self.page.locator(
                self.locators.BUILDING_VALUE
            ).first
            return building_element.is_visible()

    def check_area_info(self) -> bool:
        """
        Проверить информацию о площади.
        
        Returns:
            bool: True если информация о площади отображается
        """
        if not self.locators:
            return False
        
        with allure.step("Проверяем информацию о площади"):
            area_element = self.page.locator(self.locators.AREA_VALUE).first
            return area_element.is_visible()

    def check_view_info(self) -> bool:
        """
        Проверить информацию о виде.
        
        Returns:
            bool: True если информация о виде отображается
        """
        if not self.locators:
            return False
        
        with allure.step("Проверяем информацию о виде"):
            view_element = self.page.locator(self.locators.VIEW_VALUE).first
            return view_element.is_visible()

    def check_features(self) -> dict:
        """
        Проверить наличие особенностей апартамента.
        
        Returns:
            dict: Словарь с результатами проверки особенностей
        """
        if not self.locators:
            return {}
        
        with allure.step("Проверяем особенности апартамента"):
            features = {
                "modern_design": self.page.locator(
                    self.locators.MODERN_DESIGN
                ).first.is_visible(),
                "high_quality": self.page.locator(
                    self.locators.HIGH_QUALITY
                ).first.is_visible(),
                "built_in_appliances": self.page.locator(
                    self.locators.BUILT_IN_APPLIANCES
                ).first.is_visible(),
            }
            return features

    def check_watching_count(self) -> bool:
        """
        Проверить счетчик просмотров.
        
        Returns:
            bool: True если счетчик отображается
        """
        if not self.locators:
            return False
        
        with allure.step("Проверяем счетчик просмотров"):
            watching_element = self.page.locator(
                self.locators.WATCHING_COUNT
            ).first
            return watching_element.is_visible()

    def get_info_text(self) -> str:
        """
        Получить весь текст информации об апартаменте.
        
        Returns:
            str: Текстовое содержимое информации
        """
        if not self.locators:
            return ""
        
        with allure.step("Получаем текст информации об апартаменте"):
            info_element = self.page.locator(self.locators.INFO_CONTAINER).first
            return info_element.text_content()

    def take_info_screenshot(self):
        """
        Сделать скриншот информации об апартаменте.
        
        Returns:
            bytes: Скриншот в формате PNG
        """
        if not self.locators:
            return None
        
        with allure.step("Делаем скриншот информации"):
            info_element = self.page.locator(self.locators.INFO_CONTAINER).first
            return info_element.screenshot()

