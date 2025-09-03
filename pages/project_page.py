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
