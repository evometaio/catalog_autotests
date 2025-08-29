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
def browser_type_launch_args(browser_type):
    """Аргументы запуска браузера с учетом типа браузера."""
    headless = os.getenv("HEADLESS", "true").lower() == "true"
    
    # Специфичные аргументы для Chromium
    if browser_type.name == "chromium":
        args = ["--window-size=1920,1080", "--no-sandbox", "--disable-dev-shm-usage", "--disable-gpu", "--start-maximized"]
    # Специфичные аргументы для Firefox
    elif browser_type.name == "firefox":
        args = ["--width=1920", "--height=1080"]
    # Специфичные аргументы для WebKit - только базовые, без дополнительных флагов
    elif browser_type.name == "webkit":
        args = []
    else:
        args = []
    
    return {
        "headless": headless,
        "args": args
    }


@pytest.fixture(scope="session")
def base_url():
    """Base URL в зависимости от окружения"""
    return _get_urls_by_environment()["map"]


@pytest.fixture(scope="session")
def agent_url():
    """Base agent URL в зависимости от окружения"""
    return _get_urls_by_environment()["agent"]

def client_url():
    """Base client URL в зависимости от окружения"""
    return _get_urls_by_environment()["client"]


@pytest.fixture
def fake():
    """Фикстура для генерации тестовых данных с помощью Faker."""
    from faker import Faker
    return Faker(['ru_RU', 'en_US'])

@pytest.fixture
def map_page(page: Page, base_url):
    """Фикстура для страницы карты"""
    from pages.map_page import MapPage
    return MapPage(page, base_url)

@pytest.fixture
def project_agent_page(page: Page, agent_url):
    """Фикстура для страницы проекта (агентский роут)"""
    from pages.project_page import ProjectPage
    return ProjectPage(page, agent_url)

@pytest.fixture
def project_client_page(page: Page, client_url):
    """Фикстура для страницы проекта (клиентский роут)"""
    from pages.project_page import ProjectPage
    return ProjectPage(page, client_url)


# Хук для обработки результатов тестов
def pytest_runtest_makereport(item, call):
    """Обработчик результатов выполнения тестов."""
    if call.when == "call":
        # Сохраняем результат для использования в фикстурах
        item.rep_call = call


def _get_urls_by_environment() -> dict:
    """Получить все URL-ы для текущего окружения"""
    env = os.getenv("TEST_ENVIRONMENT", "prod")
    print(f"\n🔧 Тесты запускаются на окружении: {env.upper()}")

    # Добавляем информацию в Allure (только окружение)
    allure.dynamic.label("environment", env)

    if env == "dev":
        return {
            "map": os.getenv("DEV_BASE_URL", "https://qube-dev-next.evometa.io/map"),
            "agent": os.getenv("DEV_AGENT_BASE_URL", "https://qube-dev-next.evometa.io/agent/map"),
            "client": os.getenv("DEV_CLIENT_BASE_URL", "https://qube-dev-next.evometa.io/client/map")
        }
    else:
        return {
            "map": os.getenv("PROD_BASE_URL", "https://virtualtours.qbd.ae/map"),
            "agent": os.getenv("AGENT_PROD_BASE_URL", "https://virtualtours.qbd.ae/agent/map"),
            "client": os.getenv("CLIENT_PROD_BASE_URL", "https://virtualtours.qbd.ae/client/map")
        }