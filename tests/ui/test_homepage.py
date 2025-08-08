import allure
import pytest
from pages.home_page import HomePage


@allure.feature("Homepage")
@allure.story("Проверка главной страницы")
class TestHomepage:
    
    @pytest.fixture(autouse=True)
    def setup(self, page):
        """Инициализация страницы."""
        self.home_page = HomePage(page)

    @pytest.mark.regression
    @pytest.mark.ui
    @allure.severity(allure.severity_level.NORMAL)
    @allure.step("Тест отображения карты")
    def test_map_is_visible(self):
        """Тест отображения карты на главной странице."""
        self.home_page.open_homepage()
        pass
    
    @pytest.mark.smoke
    @pytest.mark.ui
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.step("Тест полной функциональности главной страницы")
    def test_homepage_functionality(self):
        """Комплексный тест функциональности главной страницы."""
        # Открываем страницу
        self.home_page.open_homepage()
        
        # Проверяем заголовок
        self.home_page.should_have_title("QUBE Developmen")

    
    @pytest.mark.regression
    @pytest.mark.ui
    @allure.severity(allure.severity_level.MINOR)
    @allure.step("Тест производительности загрузки страницы")
    def test_page_load_performance(self):
        """Тест производительности загрузки страницы."""
        import time
        
        start_time = time.time()
        self.home_page.open_homepage()
        load_time = time.time() - start_time
        
        # Проверяем, что страница загружается за разумное время (менее 10 секунд)
        assert load_time < 10, f"Страница загружается слишком медленно: {load_time:.2f} секунд"
        
        allure.attach(
            f"Время загрузки страницы: {load_time:.2f} секунд",
            name="page_load_time",
            attachment_type=allure.attachment_type.TEXT
        )
