import os
from datetime import datetime

import allure
import pytest
from playwright.sync_api import Page

from pages.agent_page import AgentPage
from pages.base_page import BasePage
from pages.client_page import ClientPage
from pages.project_page import ProjectPage


def _create_environment_properties():
    """Создает файл environment.properties для Allure отчета"""
    env = os.getenv("TEST_ENVIRONMENT", "prod")

    # Создаем директорию для результатов если её нет
    os.makedirs("reports/allure-results", exist_ok=True)

    # Определяем URL-ы для текущего окружения
    urls = _get_urls_by_environment()

    # Создаем содержимое файла environment.properties
    properties_content = f"""# Test Environment Configuration
                            environment = {env}
                            url = {urls['map']}
                        """

    # Записываем файл
    with open(
        "reports/allure-results/environment.properties", "w", encoding="utf-8"
    ) as f:
        f.write(properties_content)

    print(f"📝 Environment properties созданы для окружения: {env.upper()}")


@pytest.fixture(scope="session", autouse=True)
def setup_environment():
    """Фикстура для настройки окружения перед запуском тестов"""
    _create_environment_properties()
    return _get_urls_by_environment()


@pytest.fixture(autouse=True)
def setup_test_parameters(page: Page, request):
    """Устанавливает параметры OS для каждого теста и делает скриншот при падении."""
    # Устанавливаем параметры OS для Allure
    os_name = os.getenv("OS_NAME", "Unknown")
    os_platform = os.getenv("OS_PLATFORM", "Unknown")

    allure.dynamic.parameter("Operating System", os_name)
    allure.dynamic.parameter("Platform", os_platform)

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
            screenshot, name="screenshot", attachment_type=allure.attachment_type.PNG
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

    # Единые аргументы для всех браузеров
    if browser_type.name == "chromium":
        args = [
            "--no-sandbox",
            "--disable-dev-shm-usage",
        ]
    elif browser_type.name == "firefox":
        args = []
    elif browser_type.name == "webkit":
        args = []
    else:
        args = []

    return {"headless": headless, "args": args}


@pytest.fixture(scope="session")
def base_url():
    """Base URL в зависимости от окружения"""
    return _get_urls_by_environment()["map"]


@pytest.fixture(scope="session")
def agent_url():
    """Base agent URL в зависимости от окружения"""
    return _get_urls_by_environment()["agent"]


@pytest.fixture(scope="session")
def client_url():
    """Base client URL в зависимости от окружения"""
    return _get_urls_by_environment()["client"]


@pytest.fixture(scope="session")
def capstone_map_url():
    """URL карты проекта Capstone в зависимости от окружения"""
    return _get_urls_by_environment()["capstone_map"]


@pytest.fixture(scope="session")
def wellcube_map_url():
    """URL карты проекта Wellcube (Tranquil) в зависимости от окружения"""
    return _get_urls_by_environment()["wellcube_map"]


@pytest.fixture
def fake():
    """Фикстура для генерации тестовых данных с помощью Faker."""
    from faker import Faker

    return Faker(["ru_RU", "en_US"])


# Фикстуры по типам страниц
@pytest.fixture
def main_page(page: Page, request):
    """Фикстура для главных страниц (карт) всех проектов."""
    # Определяем проект из имени теста
    project_name = "qube"  # по умолчанию
    if hasattr(request, "fixturename"):
        fixture_name = request.fixturename
        if "capstone" in fixture_name:
            project_name = "capstone"
        elif "wellcube" in fixture_name:
            project_name = "wellcube"

    # Получаем URL для главной страницы
    urls = _get_urls_by_environment()

    if project_name == "capstone":
        url = urls["capstone_map"]
    elif project_name == "wellcube":
        url = urls["wellcube_map"]
    else:  # qube
        url = urls["map"]

    return BasePage(page, url)


@pytest.fixture
def agent_page(page: Page):
    """Фикстура для агентских страниц всех проектов."""
    urls = _get_urls_by_environment()
    url = urls["agent"]
    return AgentPage(page, url)


@pytest.fixture
def client_page(page: Page):
    """Фикстура для клиентских страниц всех проектов."""
    urls = _get_urls_by_environment()
    url = urls["client"]
    return ClientPage(page, url)


@pytest.fixture
def project_page(page: Page):
    """Фикстура для страниц проектов Qube."""
    urls = _get_urls_by_environment()
    url = urls["agent"]  # Используем agent URL для страниц проектов Qube
    return ProjectPage(page, url)


@pytest.fixture
def capstone_project_page(page: Page):
    """Фикстура для страниц проектов Capstone."""
    urls = _get_urls_by_environment()
    url = urls[
        "capstone_map"
    ]  # Используем capstone_map URL для страниц проектов Capstone
    return ProjectPage(page, url)


@pytest.fixture
def capstone_direct_project_page(page: Page):
    """Фикстура для прямых URL проектов Capstone (например, /project/peylaa/area)."""
    urls = _get_urls_by_environment()
    base_url = urls["capstone_map"].replace("/map", "")  # Убираем /map из базового URL
    return ProjectPage(page, base_url)


# Хук для обработки результатов тестов
def pytest_runtest_makereport(item, call):
    """Обработчик результатов выполнения тестов."""
    if call.when == "call":
        # Сохраняем результат для использования в фикстурах
        item.rep_call = call


def _get_urls_by_environment() -> dict:
    """Получить все URL-ы для текущего окружения"""
    env = os.getenv("TEST_ENVIRONMENT", "prod")

    # Добавляем информацию в Allure (только окружение)
    allure.dynamic.label("environment", env)

    if env == "dev":
        return {
            # Qube проекты (Arisha, Elire, Cubix)
            "map": os.getenv("DEV_BASE_URL", "https://qube-dev-next.evometa.io/map"),
            "agent": os.getenv(
                "DEV_AGENT_BASE_URL", "https://qube-dev-next.evometa.io/agent/map"
            ),
            "client": os.getenv(
                "DEV_CLIENT_BASE_URL", "https://qube-dev-next.evometa.io/client/map"
            ),
            # Capstone проект (Peylaa)
            "capstone_map": os.getenv(
                "DEV_CAPSTONE_BASE_URL", "https://capstone-dev.evometa.io/map"
            ),
            # Wellcube проект (Tranquil)
            "wellcube_map": os.getenv(
                "DEV_WELLCUBE_BASE_URL", "https://catalog-dev.evometa.io/wellcube/map"
            ),
        }
    else:
        return {
            # Qube проекты (Arisha, Elire, Cubix) - PROD
            "map": os.getenv("PROD_BASE_URL", "https://virtualtours.qbd.ae/map"),
            "agent": os.getenv(
                "AGENT_PROD_BASE_URL", "https://virtualtours.qbd.ae/agent/map"
            ),
            "client": os.getenv(
                "CLIENT_PROD_BASE_URL", "https://virtualtours.qbd.ae/client/map"
            ),
            # Capstone проект (Peylaa) - PROD
            "capstone_map": os.getenv(
                "CAPSTONE_PROD_BASE_URL", "https://3dtours.peylaa-phuket.com/map"
            ),
            # Wellcube проект (Tranquil) - PROD
            "wellcube_map": os.getenv(
                "WELLCUBE_PROD_BASE_URL", "https://catalog.evometa.io/wellcube/map"
            ),
        }
