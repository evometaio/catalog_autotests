from playwright.sync_api import Page

from locators.map_locators import MapLocators
from locators.project_locators import CapstonePageLocators, QubePageLocators
from pages.base_page import BasePage


class ProjectPage(BasePage):
    """
    Класс для работы со страницей проекта (агенсткий роут)
    """

    def __init__(self, page: Page, base_url: str = None):
        super().__init__(page, base_url)
        self.map_locators = MapLocators()
        self.project_locators = QubePageLocators()
        self.capstone_locators = CapstonePageLocators()

    def click_on_all_units_button(self):
        """Кликнуть на кнопку All units."""
        self.expect_visible(self.project_locators.ALL_UNITS_BUTTON)
        self.click(self.project_locators.ALL_UNITS_BUTTON)

    def click_on_residences_button_and_request_viewing_form(self):
        """Кликнуть на кнопку Residences."""
        self.expect_visible(self.project_locators.Elire.RESIDENCES_BUTTON)
        self.click(self.project_locators.Elire.RESIDENCES_BUTTON)
        self.click(self.project_locators.Elire.REQUEST_VIEWING_BUTTON)

    def click_on_sales_offer_button(self):
        """Кликнуть на кнопку Sales Offer."""
        self.expect_visible(self.project_locators.AgentPage.SALES_OFFER_BUTTON)
        self.click(self.project_locators.AgentPage.SALES_OFFER_BUTTON)

    # Методы для работы с 360 Area Tour (для всех проектов)

    def click_360_area_tour_button(self):
        """Кликнуть на кнопку 360 Area Tour."""
        # Используем универсальный локатор для всех проектов
        button_selector = '[data-test-id="nav-rotation-view-controls-button"]'
        self.expect_visible(button_selector)
        self.click(button_selector)

    def verify_360_area_tour_modal_displayed(self):
        """Проверить отображение модального окна 360 Area Tour."""
        modal_selector = "//div[contains(@class, 'modal')]"
        self.expect_visible(modal_selector)

    def verify_360_area_tour_content(self):
        """Проверить наличие контента в модальном окне 360 Area Tour."""
        # Проверяем наличие модального окна
        self.verify_360_area_tour_modal_displayed()

        # Проверяем наличие контента (изображения, видео или другие элементы)
        content_selector = "//img[contains(@class, '__react-image-turntable-img')] | //video | //canvas"
        content_element = self.page.locator(content_selector)
        assert (
            content_element.count() > 0
        ), "Контент 360 Area Tour не найден в модальном окне"
