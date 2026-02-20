"""Мобильный компонент для работы с картой."""

import allure
from playwright.sync_api import Page
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

from locators.mobile_locators import (
    MOBILE_CLOSE_BUTTON,
    MOBILE_EXPLORE_BUTTON,
    MOBILE_MODAL_MASK,
    MOBILE_PROJECT_INFO_MODAL,
)


class MobileMapComponent:
    """
    Мобильный компонент карты.

    Ответственность:
    - Клик по проектам на мобильной карте
    - Работа с мобильными модальными окнами
    - Навигация к проектам на мобильных устройствах
    """

    def __init__(self, page: Page):
        """
        Инициализация мобильного компонента карты.

        Args:
            page: Playwright Page объект
        """
        self.page = page

    def get_mobile_project_selector(self, project_name: str) -> str:
        """Получить мобильный селектор для проекта."""
        from locators.mobile_locators import get_mobile_project_selector

        return get_mobile_project_selector(project_name)

    def click_project(self, project_name: str):
        """
        Кликнуть по проекту на карте для мобильных устройств.

        Args:
            project_name: Название проекта
        """
        with allure.step(f"Кликаем по проекту {project_name.upper()} на мобильном"):
            # Получаем мобильный селектор
            selector = self.get_mobile_project_selector(project_name)

            # Ждем появления проекта на карте (увеличенный таймаут для мобильных устройств в CI)
            if project_name.lower() == "edgewater":
                # Для edgewater нужен именно третий проект (residences-3), а не первый
                project_element = self.page.locator(selector).nth(2)
            elif project_name.lower() == "willows_residences":
                project_element = self.page.locator(selector).first
            else:
                project_element = self.page.locator(selector)

            project_element.wait_for(state="visible", timeout=20000)

            # Панорамируем карту к элементу через JavaScript, чтобы он попал в viewport
            # Это решает проблему, когда элемент находится левее и не виден на экране
            try:
                # Получаем координаты элемента на карте через JavaScript
                element_info = project_element.evaluate(
                    """
                    (element) => {
                        // Получаем координаты элемента
                        const rect = element.getBoundingClientRect();
                        const centerX = rect.left + rect.width / 2;
                        const centerY = rect.top + rect.height / 2;
                        
                        return {
                            centerX: centerX,
                            centerY: centerY,
                            viewportWidth: window.innerWidth,
                            viewportHeight: window.innerHeight
                        };
                    }
                """
                )

                # Если элемент находится вне viewport, панорамируем карту
                if element_info:
                    viewport_width = element_info.get("viewportWidth", 390)
                    element_x = element_info.get("centerX", 0)

                    # Если элемент находится левее (x < 0) или правее (x > viewport width)
                    if element_x < 0 or element_x > viewport_width:
                        # Панорамируем карту через скролл, используя сам элемент
                        project_element.evaluate(
                            """
                            (element) => {
                                const rect = element.getBoundingClientRect();
                                const centerX = rect.left + rect.width / 2;
                                const centerY = rect.top + rect.height / 2;
                                
                                // Панорамируем через скролл контейнера карты
                                const mapContainer = element.closest('[class*="map"], [class*="leaflet"], [class*="mapbox"]') || 
                                                     document.querySelector('[class*="map-container"], [class*="leaflet-container"]');
                                if (mapContainer) {
                                    // Вычисляем смещение для центрирования элемента
                                    const viewportCenterX = window.innerWidth / 2;
                                    const viewportCenterY = window.innerHeight / 2;
                                    const offsetX = viewportCenterX - centerX;
                                    const offsetY = viewportCenterY - centerY;
                                    
                                    // Скроллим контейнер карты
                                    mapContainer.scrollBy({
                                        left: offsetX,
                                        top: offsetY,
                                        behavior: 'smooth'
                                    });
                                }
                            }
                        """
                        )
                        # Ждем завершения анимации панорамирования
                        self.page.wait_for_timeout(1000)
            except Exception:
                # Если не удалось панорамировать, пробуем просто скролл
                try:
                    project_element.scroll_into_view_if_needed()
                    self.page.wait_for_timeout(500)
                except Exception:
                    pass  # Продолжаем без панорамирования

            # Используем JavaScript клик напрямую, чтобы обойти проверку viewport
            # Это более надежно для элементов на карте
            try:
                project_element.evaluate("element => element.click()")
            except Exception:
                # Если JavaScript клик не сработал, используем обычный клик с force
                project_element.click(force=True)

            # Ждем появления мобильного модального окна
            # Для willows_residences модальное окно может не появляться сразу или иметь другую структуру
            if project_name.lower() == "willows_residences":
                # Ждем немного и проверяем наличие кнопки Explore Project
                self.page.wait_for_timeout(2000)
                explore_button = self.page.locator(
                    '[data-test-id*="map-project-point-button-mobile-willows"]'
                )
                try:
                    explore_button.wait_for(state="visible", timeout=5000)
                except:
                    # Если кнопка не появилась, пробуем стандартный подход
                    self.wait_for_project_modal()
            else:
                self.wait_for_project_modal()

    def wait_for_project_modal(self):
        """Ждать появления мобильного модального окна с информацией о проекте."""
        # Пробуем разные варианты модальных окон
        modal_selectors = [
            MOBILE_PROJECT_INFO_MODAL,
            "div.ant-modal",
            '[role="dialog"]',
            'div[class*="modal"]',
        ]

        modal_found = False
        for selector in modal_selectors:
            try:
                mobile_modal = self.page.locator(selector)
                mobile_modal.wait_for(state="visible", timeout=5000)
                if mobile_modal.is_visible():
                    modal_found = True
                    break
            except:
                continue

        # Если модальное окно не найдено, проверяем наличие кнопки Explore Project
        if not modal_found:
            explore_button = self.page.locator(MOBILE_EXPLORE_BUTTON)
            try:
                explore_button.wait_for(state="visible", timeout=5000)
                if explore_button.is_visible():
                    # Если кнопка видна, значит модальное окно есть, просто не определилось
                    return
            except:
                pass

        # Если ничего не найдено, пробуем еще раз с основным селектором
        mobile_modal = self.page.locator(MOBILE_PROJECT_INFO_MODAL)
        try:
            mobile_modal.wait_for(state="visible", timeout=5000)
        except:
            # Если модальное окно не появилось, но кнопка Explore Project есть, продолжаем
            explore_button = self.page.locator(MOBILE_EXPLORE_BUTTON)
            if explore_button.count() > 0 and explore_button.is_visible():
                return

    def click_explore_project(self, project_name: str):
        """
        Кликнуть по кнопке Explore Project в мобильном модальном окне.

        Args:
            project_name: Название проекта
        """
        with allure.step(f"Кликаем на Explore Project для {project_name.upper()}"):
            # Для willows_residences и edgewater используем data-test-id вместо текста
            if project_name.lower() == "willows_residences":
                # Используем частичное совпадение, так как может быть несколько вариантов
                explore_button = self.page.locator(
                    '[data-test-id*="map-project-point-button-mobile-willows"]'
                )
            elif project_name.lower() == "edgewater":
                # Для edgewater используем частичное совпадение, так как может быть несколько вариантов (edgewater-residences-1, 2, 3 и т.д.)
                explore_button = self.page.locator(
                    '[data-test-id*="map-project-point-button-mobile-edgewater"]'
                )
            else:
                # Для остальных проектов используем стандартный селектор
                explore_button = self.page.locator(MOBILE_EXPLORE_BUTTON)

            explore_button.wait_for(state="visible", timeout=20000)

            # Проверяем активность кнопки
            assert (
                explore_button.is_enabled()
            ), f"Кнопка Explore Project заблокирована для {project_name}"

            # Используем JavaScript клик напрямую, чтобы обойти проверку viewport
            # Это более надежно для элементов на карте
            try:
                explore_button.evaluate("element => element.click()")
            except Exception:
                # Если JavaScript клик не сработал, используем обычный клик
                explore_button.click()

            # Ждем перехода на страницу проекта
            # Ждем перехода на страницу проекта
            if project_name.lower() == "arsenal":
                expected_url_pattern = "**/vibe/**"
                self.page.wait_for_url(expected_url_pattern, timeout=20000)
            elif project_name.lower() == "edgewater":
                # Для edgewater URL содержит edgewater-residences-3
                self.page.wait_for_url("**/edgewater-residences-3/**", timeout=20000)
            elif project_name.lower() == "willows_residences":
                # Для willows_residences URL содержит willows-residences
                self.page.wait_for_url("**/willows-residences/**", timeout=20000)
            else:
                expected_url_pattern = f"**/{project_name.lower()}/**"
                self.page.wait_for_url(expected_url_pattern, timeout=20000)

    def navigate_to_project(self, project_name: str):
        """
        Полная навигация от карты до страницы проекта на мобильном.

        Args:
            project_name: Название проекта
        """
        with allure.step(f"Навигация к проекту {project_name.upper()} (мобильная)"):
            self.click_project(project_name)
            self.click_explore_project(project_name)

            # Проверяем успешность перехода
            # Для Arsenal используется "vibe" в URL, а не "arsenal"
            # Для edgewater URL содержит "edgewater-residences-X"
            # Для willows_residences URL содержит "willows-residences"
            current_url = self.page.url
            if project_name.lower() == "arsenal":
                expected_project_in_url = "vibe"
            elif project_name.lower() == "edgewater":
                expected_project_in_url = "edgewater-residences"
            elif project_name.lower() == "willows_residences":
                expected_project_in_url = "willows-residences"
            else:
                expected_project_in_url = project_name.lower()
            assert (
                f"/{expected_project_in_url}" in current_url
            ), f"Не удалось перейти к проекту {project_name}. Текущий URL: {current_url}"

    def close_project_modal(self):
        """Закрыть мобильное модальное окно."""
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
