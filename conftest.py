import allure
import pytest
import os
from datetime import datetime
from playwright.sync_api import Page


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
        "viewport": {"width": 1920, "height": 1080},
        "ignore_https_errors": True,
    }


@pytest.fixture(scope="session")
def browser_type_launch_args():
    """Аргументы запуска браузера."""
    return {
        "headless": os.getenv("HEADLESS", "true").lower() == "true",
        "args": ["--no-sandbox", "--disable-dev-shm-usage", "--disable-gpu"]
    }


@pytest.fixture(scope="session")
def base_url():
    """Фикстура для базового URL - требуется pytest-playwright."""
    return os.getenv("BASE_URL", "https://virtualtours.qbd.ae/map")


@pytest.fixture
def fake():
    """Фикстура для генерации тестовых данных с помощью Faker."""
    from faker import Faker
    return Faker(['ru_RU', 'en_US'])


@pytest.fixture
def dev_base_url():
    """Фикстура для DEV окружения."""
    return os.getenv("DEV_BASE_URL", "https://qube-dev-next.evometa.io/map")


@pytest.fixture
def prod_base_url():
    """Фикстура для PROD окружения."""
    return os.getenv("PROD_BASE_URL", "https://virtualtours.qbd.ae/map")


@pytest.fixture
def current_environment():
    """Фикстура для определения текущего окружения."""
    base_url = os.getenv("BASE_URL", "")
    if "dev" in base_url.lower() or "qube-dev" in base_url:
        return "dev"
    elif "prod" in base_url.lower() or "virtualtours" in base_url:
        return "prod"
    else:
        return "unknown"


@pytest.fixture
def home_page(page: Page):
    """Фикстура для главной страницы - использует POM."""
    from pages.home_page import HomePage
    base_url = os.getenv("BASE_URL", "https://virtualtours.qbd.ae/map")
    return HomePage(page, base_url)


@pytest.fixture
def home_page_dev(page: Page, dev_base_url):
    """Фикстура для главной страницы DEV окружения."""
    from pages.home_page import HomePage
    return HomePage(page, dev_base_url)


@pytest.fixture
def home_page_prod(page: Page, prod_base_url):
    """Фикстура для главной страницы PROD окружения."""
    from pages.home_page import HomePage
    return HomePage(page, prod_base_url)


# Хук для обработки результатов тестов
def pytest_runtest_makereport(item, call):
    """Обработчик результатов выполнения тестов."""
    if call.when == "call":
        # Сохраняем результат для использования в фикстурах
        item.rep_call = call


def pytest_addoption(parser):
    """Добавляет дополнительные опции командной строки."""
    parser.addoption(
        "--environment",
        action="store",
        default="dev",
        help="Окружение для тестирования (dev/prod)"
    )