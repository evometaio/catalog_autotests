import os

from playwright.sync_api import Page

from locators.map_locators import MapLocators
from locators.project_locators import QubePageLocators
from pages.base_page import BasePage


class ProjectPage(BasePage):
    """
    Класс для работы со страницей проекта (агенсткий роут)
    """

    def __init__(self, page: Page, base_url: str = None):
        super().__init__(page, base_url)
        self.map_locators = MapLocators()
        self.project_locators = QubePageLocators()


    def click_on_project(self, project_name: str):
        """Кликнуть на проект и затем на кнопку Explore Project."""
        self.wait_for_map_and_projects_loaded()
        # Сначала кликаем на проект (используем метод из MapPage)
        self.click_project(project_name)
        self.expect_visible(self.map_locators.PROJECT_INFO_WINDOW)
        self.expect_visible(self.map_locators.EXPLORE_PROJECT_BUTTON)
        # Затем кликаем на кнопку Explore Project
        self.click(self.map_locators.EXPLORE_PROJECT_BUTTON)
        self.wait_for_page_load()

    def click_on_all_units_button(self):
        """Кликнуть на кнопку All units."""
        self.expect_visible(self.project_locators.ALL_UNITS_BUTTON)
        self.click(self.project_locators.ALL_UNITS_BUTTON)

    def click_on_residences_button_and_request_viewing_form(self):
        """Кликнуть на кнопку Residences."""
        self.expect_visible(self.project_locators.Elire.RESIDENCES_BUTTON)
        self.click(self.project_locators.Elire.RESIDENCES_BUTTON)
        self.click(self.project_locators.Elire.REQUEST_VIEWING_BUTTON)


    def _find_available_apartment_generic(self):
        """Общая логика поиска доступного апартамента."""
        # Получаем все заголовки апартаментов
        apartment_titles = self.page.locator(self.project_locators.ALL_APARTMENT_TITLES)
        apartment_count = apartment_titles.count()

        if apartment_count == 0:
            raise Exception("Апартаменты не найдены на странице")

        print(f"Найдено {apartment_count} апартаментов")

        # Ищем первый доступный апартамент (без замка)
        for i in range(apartment_count):
            apartment_title = apartment_titles.nth(i)
            apartment_text = apartment_title.text_content()

            # Проверяем, есть ли замок у этого апартамента
            lock_icon = apartment_title.locator(
                "xpath=.//span[@role='img' and @aria-label='lock']"
            )
            has_lock = lock_icon.count() > 0

            print(
                f"Апартамент {apartment_text}: {'заблокирован' if has_lock else 'доступен'}"
            )

            # Если замка нет, кликаем по этому апартаменту
            if not has_lock:
                print(f"Выбираем доступный апартамент: {apartment_text}")
                apartment_title.evaluate("element => element.click()")
                return apartment_text

        # Если все апартаменты заблокированы
        raise Exception("Все апартаменты заблокированы (имеют замок)")

    def click_on_avialable_apart_on_cubix(self):
        """Обратная совместимость для Cubix."""
        return self.find_and_click_available_apartment("cubix")

    def click_on_sales_offer_button(self):
        """Кликнуть на кнопку Sales Offer."""
        self.expect_visible(self.project_locators.AgentPage.SALES_OFFER_BUTTON)
        self.click(self.project_locators.AgentPage.SALES_OFFER_BUTTON)




