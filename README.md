# Автотесты для проектов Qube, Capstone и Wellcube

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue)](https://python.org)
[![Playwright](https://img.shields.io/badge/Playwright-1.54%2B-green)](https://playwright.dev)
[![Pytest](https://img.shields.io/badge/Pytest-8.4%2B-red)](https://pytest.org)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

Автоматизированные тесты для веб-приложений проектов Qube, Capstone и Wellcube с поддержкой множественных браузеров, мобильного тестирования и интеграции с CI/CD.

## 🏗️ Архитектура

Проект построен на основе **Page Object Model** с улучшенной архитектурой:

- **Модульная структура** - четкое разделение на слои (core, config, pages, locators)
- **Система конфигурации** - поддержка .env файлов и множественных окружений
- **Улучшенные локаторы** - версионирование, fallback механизмы и метаданные
- **Обработка ошибок** - кастомные исключения и retry механизмы
- **Типизация** - полная поддержка type hints и mypy
- **Отчетность** - интеграция с Allure и автоматические скриншоты

## 📁 Структура проекта

```
autotests/
├── config/              # Конфигурационные файлы
│   ├── environments.py  # Настройки окружений
│   └── settings.py      # Глобальные настройки
├── core/               # Ядро фреймворка
│   ├── base_page.py    # Базовые классы страниц
│   ├── exceptions.py   # Кастомные исключения
│   └── decorators.py   # Полезные декораторы
├── pages/              # Page Objects
│   ├── common/         # Общие компоненты
│   ├── qube/           # Страницы проектов Qube
│   ├── capstone/       # Страницы проектов Capstone
│   └── wellcube/       # Страницы проектов Wellcube
├── locators/           # Локаторы элементов
│   ├── base_locators.py # Базовые классы локаторов
│   ├── project_locators.py # Локаторы проектов
│   └── mobile_locators.py  # Мобильные локаторы
├── utils/              # Утилиты
│   ├── api_client.py   # HTTP клиент
│   └── logger.py       # Логирование
├── tests/              # Тесты
│   ├── ui/             # UI тесты
│   └── api/            # API тесты
├── reports/            # Отчеты и скриншоты
└── docs/               # Документация
```

## 🚀 Быстрый старт

### 1. Клонирование и установка

```bash
# Клонируем репозиторий
git clone <repository-url>
cd autotests

# Устанавливаем зависимости
make install
make setup
```

### 2. Настройка окружения

```bash
# Создайте .env файл на основе .env.example
cp .env.example .env

# Редактируйте .env файл с вашими настройками
nano .env
```

Пример `.env` файла:
```env
# Окружение
TEST_ENVIRONMENT=prod
DEBUG=false
VERBOSE=false

# Браузер
HEADLESS=true
BROWSER=chromium
VIEWPORT_WIDTH=1920
VIEWPORT_HEIGHT=1080

# Таймауты
DEFAULT_TIMEOUT=10000
MAP_LOAD_TIMEOUT=20000

# Отчетность
SCREENSHOTS_ON_FAILURE=true
PAGE_SOURCE_ON_FAILURE=true
```

### 3. Запуск тестов

```bash
# Все тесты на DEV
make test-dev

# Все тесты на PROD
make test-prod

# Тесты в head режиме
make test-head-dev

# Только UI тесты
make test-ui

# Только API тесты
make test-api

# Мобильные тесты
make test-mobile-dev
```

## 🔧 Основные команды

### Тестирование

| Команда | Описание |
|---------|----------|
| `make test-dev` | Запустить все тесты на DEV |
| `make test-prod` | Запустить все тесты на PROD |
| `make test-head-dev` | UI тесты в head режиме на DEV |
| `make test-head-prod` | UI тесты в head режиме на PROD |
| `make test-ui` | Запустить все UI тесты |
| `make test-api` | Запустить все API тесты |
| `make test-mobile-dev` | Мобильные тесты на DEV |
| `make test-mobile-prod` | Мобильные тесты на PROD |
| `make regress-dev` | Полная регрессия на DEV (все браузеры) |
| `make regress-prod` | Полная регрессия на PROD (все браузеры) |

### Качество кода

| Команда | Описание |
|---------|----------|
| `make format` | Отформатировать весь код (Black + isort) |
| `make format-check` | Проверить форматирование без изменений |
| `make lint` | Проверить код линтерами (flake8) |
| `make check-deps` | Проверить зависимости |
| `make check-env` | Проверить переменные окружения |

### Отчеты и очистка

| Команда | Описание |
|---------|----------|
| `make report` | Сгенерировать Allure отчет |
| `make serve` | Запустить сервер с отчетом (http://localhost:8080) |
| `make clean` | Очистить временные файлы |

## 🎨 Форматирование кода

Проект использует автоматические форматтеры и линтеры:

- **Black** - форматирование Python кода по PEP 8
- **isort** - сортировка и группировка импортов
- **flake8** - проверка стиля кода
- **mypy** - проверка типов

```bash
# Отформатировать весь код
make format

# Проверить форматирование
make format-check

# Проверить код линтерами
make lint
```

## 🔧 Разработка

### Добавление нового теста

1. Создайте файл в соответствующей директории `tests/`
2. Используйте существующие page objects или создайте новые
3. Добавьте необходимые локаторы в `locators/`
4. Запустите тест локально:

```bash
pytest tests/your_test.py -v
```

### Создание нового page object

```python
from core.base_page import BasePage
from locators.your_locators import YourLocators

class YourPage(BasePage):
    def __init__(self, page, url):
        super().__init__(page, url, YourLocators)
    
    def your_action(self):
        self.click(self.locators.your_button)
```

### Добавление новых локаторов

```python
from locators.base_locators import BaseLocators

class YourLocators(BaseLocators):
    def _register_locators(self):
        self._add_locator(
            "YOUR_BUTTON",
            "button[data-test-id='your-button']",
            "Кнопка для вашего действия",
            fallback="button:has-text('Your Button')"
        )
```

## 🐛 Troubleshooting

### Частые проблемы

#### Тесты падают с TimeoutError
- Проверьте доступность тестируемого сайта
- Увеличьте таймауты в `.env` файле
- Проверьте стабильность локаторов

#### Проблемы с мобильным тестированием
- Убедитесь, что Playwright установлен с мобильными устройствами
- Проверьте настройки viewport в `.env` файле

#### Ошибки конфигурации
- Проверьте наличие `.env` файла
- Убедитесь в корректности URL'ов в конфигурации
- Запустите `make check-env` для диагностики

#### Проблемы с локаторами
- Используйте fallback селекторы
- Проверьте метаданные локаторов
- Включите debug режим в `.env`

### Отладка

```bash
# Запуск с подробным логированием
DEBUG=true VERBOSE=true pytest tests/your_test.py -v -s

# Запуск в head режиме для визуальной отладки
HEADLESS=false pytest tests/your_test.py -v -s

# Запуск конкретного теста
pytest tests/ui/qube/arisha/test_arisha_map.py::TestArishaMap::test_arisha_map -v
```

## 📊 Отчеты

Отчеты генерируются в формате Allure и содержат:

- Детальную информацию о выполнении тестов
- Скриншоты при падениях
- Логи выполнения
- Метаданные окружения
- История выполнения

### Просмотр отчетов

```bash
# Генерация отчета
make report

# Запуск локального сервера
make serve
# Открыть http://localhost:8080
```

### CI/CD отчеты

Отчеты автоматически публикуются на GitHub Pages:
- **Локально**: `make serve`
- **CI/CD**: GitHub Pages (ссылка в README)

## 🚀 CI/CD интеграция

### GitHub Actions

Проект настроен для автоматического запуска тестов через GitHub Actions:

#### Автоматические запуски
- **По расписанию**: каждый день в 11:00 МСК
- **При push в main**: полный набор тестов
- **При PR**: smoke тесты

#### Ручной запуск

1. Перейти в раздел **Actions** → **Tests CI Pipeline**
2. Нажать **Run workflow**
3. Выбрать параметры:
   - **Branch**: `main` (или другая ветка)
   - **Environment**: `prod` или `dev`
   - **Run type**: `smoke`, `regression` или `full`

#### Быстрые ссылки

##### 🟢 PRODUCTION окружение
[![Run Tests on PROD](https://img.shields.io/badge/Run_Tests_on_PROD-00ff00?style=for-the-badge&logo=github)](https://github.com/username/repo/actions/workflows/cicd.yml?query=event%3Aworkflow_dispatch)

##### 🟡 DEVELOPMENT окружение
[![Run Tests on DEV](https://img.shields.io/badge/Run_Tests_on_DEV-ffff00?style=for-the-badge&logo=github)](https://github.com/username/repo/actions/workflows/cicd.yml?query=event%3Aworkflow_dispatch)

## 🤝 Вклад в проект

1. Создайте feature branch
2. Внесите изменения
3. Добавьте тесты для новой функциональности
4. Запустите проверки качества кода:
   ```bash
   make format
   make lint
   make test-dev
   ```
5. Создайте Pull Request

### Стандарты кода

- Используйте type hints для всех функций
- Добавляйте docstrings для публичных методов
- Следуйте принципам SOLID
- Покрывайте новую функциональность тестами
- Используйте meaningful имена для переменных и функций

## 📝 Лицензия

Этот проект лицензирован под MIT License - см. файл [LICENSE](LICENSE) для деталей.

## 📞 Поддержка

Если у вас есть вопросы или проблемы:

1. Проверьте [Troubleshooting](#-troubleshooting)
2. Создайте [Issue](https://github.com/company/autotests/issues)
3. Обратитесь к команде QA

