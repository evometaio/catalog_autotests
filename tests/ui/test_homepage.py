"""
Тесты для главной страницы.
Использует Page Object Model (POM) с HomePage.
"""
import allure
import pytest
from pages.home_page import HomePage


@allure.feature("Главная страница")
@allure.story("Загрузка страницы")
@pytest.mark.smoke
@pytest.mark.ui
@allure.severity(allure.severity_level.CRITICAL)
def test_homepage_loads(page, base_url):
    """Тест загрузки главной страницы."""
    home_page = HomePage(page, base_url)
    
    with allure.step("Открываем главную страницу"):
        home_page.open_homepage()
    
    with allure.step("Проверяем наличие карты"):
        home_page.check_map_visible()


@allure.feature("Главная страница")
@allure.story("Элементы страницы")
@pytest.mark.regression
@pytest.mark.ui
@allure.severity(allure.severity_level.NORMAL)
def test_page_elements(page, base_url):
    """Тест наличия основных элементов страницы."""
    home_page = HomePage(page, base_url)
    
    with allure.step("Открываем главную страницу"):
        home_page.open_homepage()
    
    with allure.step("Проверяем наличие всех основных элементов"):
        home_page.check_all_elements()


@allure.feature("Главная страница")
@allure.story("URL страницы")
@pytest.mark.smoke
@pytest.mark.ui
@allure.severity(allure.severity_level.CRITICAL)
def test_page_url(page, base_url):
    """Тест корректности URL страницы."""
    with allure.step(f"Переходим на {base_url}"):
        page.goto(base_url)
    
    with allure.step("Проверяем URL"):
        assert page.url == base_url, f"Ожидался URL: {base_url}, получен: {page.url}"


@allure.feature("Главная страница")
@allure.story("Генерация данных")
@pytest.mark.regression
@allure.severity(allure.severity_level.MINOR)
def test_with_fake_data(fake):
    """Тест с использованием генерации тестовых данных."""
    with allure.step("Генерация тестовых данных"):
        name = fake.name()
        email = fake.email()
        phone = fake.phone_number()
    
    with allure.step("Проверка корректности данных"):
        assert name, "Имя не должно быть пустым"
        assert "@" in email, "Email должен содержать @"
        assert len(phone) > 10, "Телефон должен быть корректной длины"


@allure.feature("Главная страница")
@allure.story("POM функциональность")
@pytest.mark.regression
@pytest.mark.ui
@allure.severity(allure.severity_level.NORMAL)
def test_homepage_pom_functionality(page, base_url):
    """Тест функциональности POM для главной страницы."""
    home_page = HomePage(page, base_url)
    
    with allure.step("Открываем главную страницу"):
        home_page.open_homepage()
    
    with allure.step("Проверяем базовые методы POM"):
        # Проверяем, что базовые методы работают
        assert home_page.is_visible("div#map"), "Карта должна быть видима"
        assert home_page.get_text("header") is not None, "Заголовок должен содержать текст"
