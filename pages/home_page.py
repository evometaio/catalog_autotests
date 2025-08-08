import allure
from playwright.sync_api import expect
from pages.base_page import BasePage


class HomePage(BasePage):
    URL = "https://virtualtours.qbd.ae/map"

    def open_homepage(self):
        with allure.step("Открываем главную страницу"):
            self.open()
            with allure.step(f"Проверяем что URL соответствует {self.URL}"):
                expect(self.page).to_have_url(self.URL)

    def should_have_title(self, expected_title: str):
        with allure.step(f"Проверяем заголовок страницы: '{expected_title}'"):
            expect(self.page).to_have_title(expected_title)
            allure.attach(
                f"Фактический заголовок соответствует ожидаемому: '{expected_title}'",
                name="Title verification",
                attachment_type=allure.attachment_type.TEXT
            )

    def map_should_be_visible(self):
        with allure.step("Проверяем отображение карты"):
            map_element = self.page.locator("div#map")
            with allure.step("Находим элемент карты на странице"):
                expect(map_element).to_be_visible()
                with allure.step("Делаем скриншот карты"):
                    screenshot = map_element.screenshot()
                    allure.attach(
                        screenshot,
                        name="map_screenshot",
                        attachment_type=allure.attachment_type.PNG
                    )