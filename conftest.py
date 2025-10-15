import os
from datetime import datetime

import allure
import pytest
from dotenv import load_dotenv
from playwright.sync_api import Page

# Загружаем переменные из .env файла
load_dotenv()

from locators.qube.arisha_locators import ArishaLocators
from locators.qube.elire_locators import ElireLocators
from locators.qube.cubix_locators import CubixLocators
from locators.capstone.peylaa_locators import PeylaaLocators
from locators.wellcube.tranquil_locators import TranquilLocators
from locators.base_locators import BaseLocators
from pages.base_page import BasePage

# ==================== МОБИЛЬНЫЕ УСТРОЙСТВА ====================

MOBILE_DEVICES = {
    "iphone_13": {
        "viewport": {"width": 390, "height": 844},
        "device_scale_factor": 3,
        "is_mobile": True,
        "has_touch": True,
        "user_agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
    },
    "pixel_5": {
        "viewport": {"width": 393, "height": 851},
        "device_scale_factor": 2.75,
        "is_mobile": True,
        "has_touch": True,
        "user_agent": "Mozilla/5.0 (Linux; Android 11; Pixel 5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36",
    },
}


def _create_environment_properties():
    """Создает файл environment.properties для Allure отчета"""
    env = os.getenv("TEST_ENVIRONMENT", "prod")
    device = os.getenv("MOBILE_DEVICE", "desktop")

    # Создаем директорию для результатов если её нет
    os.makedirs("reports/allure-results", exist_ok=True)

    # Определяем URL-ы для текущего окружения
    urls = _get_urls_by_environment()

    # Создаем содержимое файла environment.properties
    properties_content = f"""# Test Environment Configuration
                            environment = {env}
                            device = {device}
                            url = {urls['map']}
                        """

    # Записываем файл
    with open(
        "reports/allure-results/environment.properties", "w", encoding="utf-8"
    ) as f:
        f.write(properties_content)

    print(
        f"📝 Environment properties созданы для окружения: {env.upper()}, устройство: {device}"
    )


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
    device = os.getenv("MOBILE_DEVICE", "desktop")

    allure.dynamic.parameter("Operating System", os_name)
    allure.dynamic.parameter("Platform", os_platform)
    allure.dynamic.parameter("Device", device)

    # Добавляем информацию об устройстве в Allure
    if device != "desktop":
        allure.dynamic.label("device", device)
        if device in MOBILE_DEVICES:
            mobile_config = MOBILE_DEVICES[device]
            allure.dynamic.parameter(
                "Viewport",
                f"{mobile_config['viewport']['width']}x{mobile_config['viewport']['height']}",
            )

    yield

    if request.node.rep_call.failed:
        # Создаем директорию для скриншотов если её нет
        os.makedirs("reports/screenshots", exist_ok=True)

        # Генерируем имя файла
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        test_name = request.node.name.replace("/", "_").replace("\\", "_")
        screenshot_name = f"{device}_{test_name}_{timestamp}.png"
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
    """Настройки контекста браузера с поддержкой мобильных устройств."""
    device = os.getenv("MOBILE_DEVICE", "desktop")

    # Если указано мобильное устройство, используем его настройки
    if device != "desktop" and device in MOBILE_DEVICES:
        mobile_config = MOBILE_DEVICES[device]
        return {
            **browser_context_args,
            "viewport": mobile_config["viewport"],
            "device_scale_factor": mobile_config["device_scale_factor"],
            "is_mobile": mobile_config["is_mobile"],
            "has_touch": mobile_config["has_touch"],
            "user_agent": mobile_config["user_agent"],
            "ignore_https_errors": True,
            "accept_downloads": True,
        }
    else:
        # Десктопная конфигурация
        return {
            **browser_context_args,
            "viewport": {"width": 1920, "height": 1080},
            "ignore_https_errors": True,
            "accept_downloads": True,
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
def map_page(page: Page, request):
    """Фикстура для карт всех проектов."""
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
        return BasePage(page, url, PeylaaLocators)
    elif project_name == "wellcube":
        url = urls["wellcube_map"]
        return BasePage(page, url, TranquilLocators)
    else:  # qube
        url = urls["map"]
        return BasePage(page, url, BaseLocators)


@pytest.fixture
def agent_page(page: Page):
    """Фикстура для агентских страниц всех проектов."""
    urls = _get_urls_by_environment()
    url = urls["agent"]
    return BasePage(page, url, BaseLocators)


@pytest.fixture
def client_page(page: Page):
    """Фикстура для клиентских страниц всех проектов."""
    urls = _get_urls_by_environment()
    url = urls["client"]
    return BasePage(page, url, BaseLocators)




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


# ==================== УТИЛИТЫ ДЛЯ МОБИЛЬНОГО ТЕСТИРОВАНИЯ ====================


def get_mobile_device_config(device_name: str) -> dict:
    """Получить конфигурацию мобильного устройства."""
    return MOBILE_DEVICES.get(device_name, MOBILE_DEVICES["iphone_13"])


def get_available_devices() -> list:
    """Получить список доступных мобильных устройств."""
    return list(MOBILE_DEVICES.keys())


def _get_mobile_base_url(route_type: str = "map", project_type: str = "qube") -> str:
    """
    Вспомогательная функция для получения base_url для мобильных фикстур.
    
    Args:
        route_type: Тип роута ("map", "agent", "client")
        project_type: Тип проекта ("qube", "capstone", "wellcube")
    
    Returns:
        str: Base URL для указанного окружения
    """
    environment = os.getenv("TEST_ENVIRONMENT", "dev")
    urls = _get_urls_by_environment()
    
    if project_type == "capstone":
        return urls["capstone_map"]
    elif project_type == "wellcube":
        return urls["wellcube_map"]
    else:  # qube
        if route_type == "agent":
            return urls["agent"]
        elif route_type == "client":
            return urls["client"]
        else:  # map
            return urls["map"]


@pytest.fixture(scope="function")
def mobile_device_info():
    """Фикстура для получения информации о текущем мобильном устройстве."""
    device = os.getenv("MOBILE_DEVICE", "iphone_13")
    config = get_mobile_device_config(device)

    return {
        "name": device,
        "viewport": config["viewport"],
        "user_agent": config["user_agent"],
        "is_mobile": config["is_mobile"],
        "has_touch": config["has_touch"],
    }


@pytest.fixture
def mobile_page(page, request):
    """Фикстура для MobilePage с картой."""
    from pages.mobile.mobile_page import MobilePage

    # Определяем проект из имени теста
    test_file = request.fspath.basename
    
    if "capstone" in test_file or "peylaa" in test_file:
        project_type = "capstone"
        locators = PeylaaLocators()
    elif "wellcube" in test_file or "tranquil" in test_file:
        project_type = "wellcube"
        locators = TranquilLocators()
    else:
        project_type = "qube"
        locators = BaseLocators()
    
    # Создаем страницу с правильным URL и локаторами
    mobile_page = MobilePage(page)
    mobile_page.base_url = _get_mobile_base_url("map", project_type)
    mobile_page.project_locators = locators
    
    return mobile_page


@pytest.fixture
def mobile_agent_page(page):
    """Фикстура для MobilePage с агентским роутом."""
    from pages.mobile.mobile_page import MobilePage

    mobile_page = MobilePage(page)
    mobile_page.base_url = _get_mobile_base_url("agent", "qube")
    mobile_page.project_locators = BaseLocators()
    return mobile_page


@pytest.fixture
def mobile_client_page(page):
    """Фикстура для MobilePage с клиентским роутом."""
    from pages.mobile.mobile_page import MobilePage

    mobile_page = MobilePage(page)
    mobile_page.base_url = _get_mobile_base_url("client", "qube")
    mobile_page.project_locators = BaseLocators()
    return mobile_page


# ==================== НОВЫЕ ФИКСТУРЫ С УЛУЧШЕННОЙ АРХИТЕКТУРОЙ ====================

@pytest.fixture
def arisha_page(page: Page):
    """Фикстура для страницы Arisha с новой архитектурой."""
    from pages.projects.qube.arisha_page import ArishaPage
    return ArishaPage(page)


@pytest.fixture
def elire_page(page: Page):
    """Фикстура для страницы Elire с новой архитектурой."""
    from pages.projects.qube.elire_page import ElirePage
    return ElirePage(page)


@pytest.fixture
def cubix_page(page: Page):
    """Фикстура для страницы Cubix с новой архитектурой."""
    from pages.projects.qube.cubix_page import CubixPage
    return CubixPage(page)


@pytest.fixture
def peylaa_page(page: Page):
    """Фикстура для страницы Peylaa с новой архитектурой."""
    from pages.projects.capstone.peylaa_page import PeylaaPage
    return PeylaaPage(page)


@pytest.fixture
def tranquil_page(page: Page):
    """Фикстура для страницы Tranquil с новой архитектурой."""
    from pages.projects.wellcube.tranquil_page import TranquilPage
    return TranquilPage(page)
