"""
Оптимизированная конфигурация pytest с только используемыми фикстурами.
"""

import os
from datetime import datetime
from typing import Any, Dict

import allure
import pytest
from playwright.sync_api import Page, sync_playwright

from config.environments import EnvironmentConfig, environment_manager
from config.settings import settings
from core.exceptions import EnvironmentError
from locators import locators
from utils.logger import get_logger

logger = get_logger(__name__)


def _validate_environment() -> None:
    """Валидирует настройки окружения."""
    try:
        environment_manager.validate_current_environment()
        logger.info("Окружение валидировано успешно")
    except EnvironmentError as e:
        logger.error(f"Ошибка валидации окружения: {e}")
        raise


def _create_environment_properties() -> None:
    """Создает файл environment.properties для Allure отчета."""
    env_config = environment_manager.get_environment()

    # Создаем директорию для результатов если её нет
    os.makedirs(settings.reporting.allure_results_dir, exist_ok=True)

    # Создаем содержимое файла environment.properties
    properties_content = f"""# Test Environment Configuration
environment = {env_config.name}
base_url = {env_config.base_url}
agent_url = {env_config.agent_url}
client_url = {env_config.client_url}
capstone_map_url = {env_config.capstone_map_url}
wellcube_map_url = {env_config.wellcube_map_url}
timeout = {env_config.timeout}
verify_ssl = {env_config.verify_ssl}
timestamp = {datetime.now().isoformat()}
"""

    # Записываем в файл
    properties_file = os.path.join(
        settings.reporting.allure_results_dir, "environment.properties"
    )
    with open(properties_file, "w", encoding="utf-8") as f:
        f.write(properties_content)

    logger.info(f"Создан файл environment.properties: {properties_file}")


# ================================
# СЕССИОННЫЕ ФИКСТУРЫ
# ================================


@pytest.fixture(scope="session", autouse=True)
def setup_environment() -> EnvironmentConfig:
    """Настройка окружения для тестов."""
    logger.info("Настройка окружения для тестов...")

    # Валидируем окружение
    _validate_environment()

    # Получаем конфигурацию окружения
    env_config = environment_manager.get_environment()

    # Создаем файл properties для Allure
    _create_environment_properties()

    logger.info(f"Окружение настроено: {env_config.name}")
    return env_config


@pytest.fixture(autouse=True)
def setup_test_parameters(page: Page, request) -> None:
    """Настройка параметров теста."""
    test_name = request.node.name

    # Устанавливаем параметры для Allure
    allure.dynamic.parameter("Test Name", test_name)
    allure.dynamic.parameter("Browser", "Chromium")
    allure.dynamic.parameter(
        "Viewport",
        f"{settings.browser.viewport_width}x{settings.browser.viewport_height}",
    )

    logger.info(f"Настройка параметров для теста: {test_name}")


@pytest.fixture(autouse=True)
def _take_screenshot_on_failure(page: Page, request) -> None:
    """Автоматически делает скриншот при падении теста."""
    yield

    if request.node.rep_call.failed:
        try:
            # Создаем директорию для скриншотов
            screenshots_dir = "reports/screenshots"
            os.makedirs(screenshots_dir, exist_ok=True)

            # Генерируем имя файла
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            test_name = request.node.name
            screenshot_path = os.path.join(
                screenshots_dir, f"{test_name}_{timestamp}.png"
            )

            # Делаем скриншот
            page.screenshot(path=screenshot_path)

            # Прикрепляем к Allure отчету
            allure.attach.file(
                screenshot_path,
                name="Screenshot on Failure",
                attachment_type=allure.attachment_type.PNG,
            )

            logger.info(f"Скриншот сохранен: {screenshot_path}")

        except Exception as e:
            logger.error(f"Ошибка при создании скриншота: {e}")


# ================================
# БРАУЗЕРНЫЕ ФИКСТУРЫ
# ================================


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args) -> Dict[str, Any]:
    """Настройки контекста браузера."""
    return {
        **browser_context_args,
        "viewport": {
            "width": settings.browser.viewport_width,
            "height": settings.browser.viewport_height,
        },
        "ignore_https_errors": settings.browser.ignore_https_errors,
    }


@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type) -> Dict[str, Any]:
    """Аргументы запуска браузера с учетом типа браузера."""
    return {
        "headless": settings.browser.headless,
        "args": settings.get_browser_args(browser_type.name),
    }


# ================================
# ДАННЫЕ И УТИЛИТЫ
# ================================


@pytest.fixture
def fake():
    """Фикстура для генерации тестовых данных с помощью Faker."""
    from faker import Faker

    fake = Faker("en_US")
    return fake


# ================================
# PAGE OBJECT ФИКСТУРЫ
# ================================


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
    env_config = environment_manager.get_environment()

    if project_name == "capstone":
        from pages.capstone.capstone_pages import CapstonePages

        return CapstonePages(page, env_config.capstone_map_url)
    elif project_name == "wellcube":
        from pages.wellcube.wellcube_pages import WellcubePages

        return WellcubePages(page, env_config.wellcube_map_url)
    else:  # qube
        from pages.qube.qube_map_page import QubeMapPage

        return QubeMapPage(page, env_config.base_url)


@pytest.fixture
def agent_page(page: Page):
    """Фикстура для агентских страниц всех проектов."""
    from pages.qube.agent_page import AgentPage

    env_config = environment_manager.get_environment()
    return AgentPage(page, env_config.agent_url)


@pytest.fixture
def client_page(page: Page):
    """Фикстура для клиентских страниц всех проектов."""
    from pages.qube.client_page import ClientPage

    env_config = environment_manager.get_environment()
    return ClientPage(page, env_config.client_url)


@pytest.fixture
def capstone_project_page(page: Page):
    """Фикстура для страниц проектов Capstone."""
    from pages.capstone.capstone_pages import CapstonePages

    return CapstonePages(page)


@pytest.fixture
def wellcube_page(page: Page):
    """Фикстура для страниц Wellcube проектов."""
    from pages.wellcube.wellcube_pages import WellcubePages

    return WellcubePages(page)


# ================================
# МОБИЛЬНЫЕ ФИКСТУРЫ
# ================================


@pytest.fixture
def mobile_map_page(page: Page, request):
    """Фикстура для мобильных карт всех проектов."""
    # Применяем мобильные настройки
    page.set_viewport_size(
        {
            "width": settings.mobile.viewport_width,
            "height": settings.mobile.viewport_height,
        }
    )

    # Устанавливаем мобильный User-Agent
    page.context.set_extra_http_headers({"User-Agent": settings.mobile.user_agent})

    # Устанавливаем параметры для Allure
    allure.dynamic.parameter("Device", settings.mobile.device_type)
    allure.dynamic.parameter(
        "Viewport",
        f"{settings.mobile.viewport_width}x{settings.mobile.viewport_height}",
    )
    allure.dynamic.parameter("Mobile", "True")

    # Определяем проект из имени теста
    project_name = "qube"  # по умолчанию
    if hasattr(request, "fixturename"):
        fixture_name = request.fixturename
        if "capstone" in fixture_name:
            project_name = "capstone"
        elif "wellcube" in fixture_name:
            project_name = "wellcube"

    # Получаем URL для главной страницы
    env_config = environment_manager.get_environment()

    if project_name == "capstone":
        from pages.capstone.capstone_pages import CapstonePages

        return CapstonePages(page, env_config.capstone_map_url)
    elif project_name == "wellcube":
        from pages.wellcube.wellcube_pages import WellcubePages

        return WellcubePages(page, env_config.wellcube_map_url)
    else:  # qube
        from core.base_page import BasePage

        return BasePage(page, env_config.base_url)


# ================================
# PLAYWRIGHT ФИКСТУРЫ
# ================================


@pytest.fixture(scope="session")
def playwright():
    """Фикстура для Playwright."""
    with sync_playwright() as p:
        yield p


@pytest.fixture(scope="session")
def browser(playwright):
    """Фикстура для браузера."""
    browser = playwright.chromium.launch(
        headless=settings.browser.headless,
        args=settings.get_browser_args("chromium"),
    )
    yield browser
    browser.close()


# ================================
# PYTEST ХУКИ
# ================================


def pytest_runtest_makereport(item, call):
    """Создает отчет о выполнении теста для скриншотов."""
    if "page" in item.fixturenames:
        item.rep_call = call


def pytest_configure(config):
    """Конфигурация pytest."""
    config.addinivalue_line("markers", "smoke: smoke tests")
    config.addinivalue_line("markers", "regression: regression tests")
    config.addinivalue_line("markers", "ui: ui tests")
    config.addinivalue_line("markers", "api: api tests")
    config.addinivalue_line("markers", "mobile: mobile tests")


def pytest_collection_modifyitems(config, items):
    """Модифицирует коллекцию тестов."""
    # Добавляем маркеры на основе пути к файлу
    for item in items:
        if "mobile" in str(item.fspath):
            item.add_marker(pytest.mark.mobile)
        if "api" in str(item.fspath):
            item.add_marker(pytest.mark.api)
        if "ui" in str(item.fspath):
            item.add_marker(pytest.mark.ui)
