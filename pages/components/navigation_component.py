"""Компонент для навигации по зданиям, этажам и апартаментам."""

import allure
from playwright.sync_api import Page


class NavigationComponent:
    """
    Компонент навигации.

    Ответственность:
    - Навигация по зданиям
    - Навигация по этажам
    - Навигация по апартаментам
    - Работа с планами этажей
    """

    def __init__(self, page: Page, project_locators):
        """
        Инициализация компонента навигации.

        Args:
            page: Playwright Page объект
            project_locators: Локаторы проекта
        """
        self.page = page
        self.locators = project_locators

    def navigate_to_building(self, building_number: int) -> str:
        """
        Переход к зданию через навигационное меню.

        Args:
            building_number: Номер здания (1, 2, 3...)

        Returns:
            str: URL после перехода к зданию
        """
        with allure.step(f"Переходим к зданию {building_number}"):
            # Кликаем на навигацию по зданиям
            building_nav = self.page.locator(self.locators.BUILDING_NAV_BUTTON)
            building_nav.click()

            # Формируем селектор кнопки здания
            building_button = f'[data-test-id="nav-desktop-building-{building_number}"]'

            # Ждем появления и стабилизации дропдауна
            self.page.wait_for_selector(building_button, state="visible", timeout=5000)

            button = self.page.locator(building_button)
            button.click()

            # Ждем изменения URL
            self.page.wait_for_url(f"**/building/{building_number}", timeout=10000)

            current_url = self.page.url
            allure.attach(
                f"URL после выбора здания {building_number}: {current_url}",
                name=f"Building {building_number} URL",
            )
            return current_url

    def navigate_to_floor(self, floor_number: int) -> str:
        """
        Переход к этажу через навигационное меню.

        Args:
            floor_number: Номер этажа (1, 2, 3...)

        Returns:
            str: URL после перехода к этажу
        """
        with allure.step(f"Переходим к этажу {floor_number}"):
            # Кликаем на навигацию по этажам
            floor_nav = self.page.locator(self.locators.FLOOR_NAV_BUTTON)
            floor_nav.click()

            # Формируем селектор кнопки этажа
            floor_button = f'[data-test-id="nav-desktop-floor-{floor_number}"]'

            # Ждем появления и стабилизации дропдауна
            self.page.wait_for_selector(floor_button, state="visible", timeout=5000)
            self.page.wait_for_timeout(500)  # Ждем завершения анимации

            button = self.page.locator(floor_button)
            button.click()

            # Ждем изменения URL
            self.page.wait_for_url(f"**/floor/*/{floor_number}", timeout=10000)

            current_url = self.page.url
            allure.attach(
                f"URL после выбора этажа {floor_number}: {current_url}",
                name=f"Floor {floor_number} URL",
            )
            return current_url

    def navigate_to_floor_direct(
        self, project_name: str, building_number: int, floor_number: int, base_url: str
    ) -> str:
        """
        Прямой переход к этажу через URL (без использования навигации).

        Args:
            project_name: Название проекта (arisha, elire, cubix...)
            building_number: Номер здания
            floor_number: Номер этажа
            base_url: Базовый URL приложения

        Returns:
            str: URL после перехода
        """
        with allure.step(
            f"Прямой переход к этажу {floor_number} здания {building_number}"
        ):
            floor_url = base_url.replace(
                "/map",
                f"/project/{project_name}/floor/{building_number}/{floor_number}",
            )
            self.page.goto(floor_url)
            self.page.wait_for_timeout(1000)

            current_url = self.page.url
            allure.attach(
                f"URL этажа {floor_number}: {current_url}",
                name=f"Floor {floor_number} URL",
            )
            return current_url

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
            apartment_selector = self.locators.FLOOR_PLAN_APARTMENTS

        with allure.step("Ищем и кликаем на доступный апартамент"):
            # Ждем загрузки апартаментов
            self.page.wait_for_selector(apartment_selector, timeout=10000)

            apartment_elements = self.page.locator(apartment_selector)
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
                        # Небольшая пауза после клика
                        self.page.wait_for_timeout(500)
                        return True

                except Exception:
                    continue

            return False

    def click_apartment_on_floor(self) -> bool:
        """
        Клик на доступный апартамент на текущем этаже.

        Returns:
            bool: True если удалось кликнуть на апартамент
        """
        with allure.step("Кликаем на апартамент на плане этажа"):
            # Ждем загрузки плана этажа
            self.page.wait_for_selector(
                self.locators.FLOOR_PLAN_APARTMENTS, timeout=10000
            )

            # Получаем количество апартаментов
            apartment_elements = self.page.locator(self.locators.FLOOR_PLAN_APARTMENTS)
            apartment_count = apartment_elements.count()
            allure.attach(
                f"Найдено апартаментов на этаже: {apartment_count}",
                name="Apartment Count",
            )

            # Кликаем на первый доступный апартамент
            result = self.click_available_apartment()

            if result:
                current_url = self.page.url
                allure.attach(
                    f"URL после клика на апартамент: {current_url}",
                    name="Apartment URL",
                )

            return result

    def find_and_click_available_apartment(self, project_name: str = None):
        """
        Найти и кликнуть на первый доступный апартамент (без замка) в каталоге.

        Args:
            project_name: Название проекта (используется только для логирования)
        """
        with allure.step("Ищем доступный апартамент в каталоге"):
            self.page.wait_for_timeout(3500)

            # Ищем все апартаменты
            apartment_titles = self.page.locator(self.locators.ALL_APARTMENT_TITLES)

            # Явно ждем появления хотя бы одного апартамента (важно для CI)
            try:
                apartment_titles.first.wait_for(state="attached", timeout=15000)
            except Exception:
                # Если не дождались, пробуем еще раз с небольшим ожиданием
                self.page.wait_for_timeout(2000)

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
                    allure.attach(
                        f"Выбран апартамент: {apartment_text}",
                        name="Selected Apartment",
                    )
                    return apartment_text

            # Если не найден ни один доступный апартамент
            raise AssertionError(
                f"Не найден ни один доступный апартамент для проекта {project_name}"
            )
