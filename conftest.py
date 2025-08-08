import allure
import pytest
import os
from datetime import datetime
from playwright.sync_api import Page
from utils.logger import setup_logger


@pytest.fixture(scope="session", autouse=True)
def setup_logging():
    """Настройка логирования для всей сессии тестов."""
    setup_logger("autotests", "INFO")
    yield


@pytest.fixture(autouse=True)
def screenshot_on_failure(page: Page, request):
    """Делает скриншот при падении теста."""
    yield
    if request.node.rep_call.failed:
        # Создаем директорию для скриншотов если её нет
        os.makedirs("reports/screenshots", exist_ok=True)
        
        # Генерируем имя файла
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        test_name = request.node.name.replace("/", "_").replace("\\", "_")
        screenshot_name = f"{test_name}_{timestamp}.png"
        screenshot_path = os.path.join("reports/screenshots", screenshot_name)
        
        # Делаем скриншот
        screenshot = page.screenshot()
        
        # Сохраняем файл
        with open(screenshot_path, "wb") as f:
            f.write(screenshot)
        
        # Прикрепляем к Allure отчету
        allure.attach(
            screenshot,
            name="screenshot",
            attachment_type=allure.attachment_type.PNG
        )


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """Настройки контекста браузера."""
    return {
        **browser_context_args,
        "viewport": {
            "width": 1920,
            "height": 1080,
        },
        "ignore_https_errors": True,
    }


@pytest.fixture(scope="session")
def browser_type_launch_args():
    """Аргументы запуска браузера."""
    return {
        "headless": True,
        "args": [
            "--no-sandbox",
            "--disable-dev-shm-usage",
            "--disable-gpu",
        ]
    }


@pytest.fixture
def api_client():
    """Фикстура для API клиента."""
    from utils.api_client import APIClient
    return APIClient()


@pytest.fixture
def fake():
    """Фикстура для генерации тестовых данных с помощью Faker."""
    from faker import Faker
    return Faker(['ru_RU', 'en_US'])


@pytest.fixture
def test_data():
    """Фикстура с тестовыми данными."""
    from faker import Faker
    fake = Faker(['ru_RU', 'en_US'])
    
    return {
        "valid_user": {
            "username": fake.user_name(),
            "email": fake.email(),
            "password": fake.password(length=12),
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
        }
    }

# Хук для обработки результатов тестов
def pytest_runtest_makereport(item, call):
    """Обработчик результатов выполнения тестов."""
    if call.when == "call":
        # Сохраняем результат для использования в фикстурах
        item.rep_call = call