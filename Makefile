.PHONY: help install setup test clean report check-deps check-env format lint

# Переменные
PYTHON = python3
PIP = pip3
PYTEST = pytest
ALLURE = allure
BLACK = black
ISORT = isort
FLAKE8 = flake8

# Цвета
GREEN = \033[0;32m
YELLOW = \033[1;33m
RED = \033[0;31m
BLUE = \033[0;34m
NC = \033[0m

help: ## Показать справку
	@echo "$(GREEN)🚀 Autotests - Доступные команды:$(NC)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(YELLOW)%-20s$(NC) %s\n", $$1, $$2}'

check-deps: ## Проверить зависимости
	@echo "$(BLUE)🔍 Проверка зависимостей...$(NC)"
	@which $(PYTHON) > /dev/null || (echo "$(RED)❌ Python3 не найден$(NC)" && exit 1)
	@which $(PIP) > /dev/null || (echo "$(RED)❌ pip3 не найден$(NC)" && exit 1)
	@test -f requirements.txt || (echo "$(RED)❌ requirements.txt не найден$(NC)" && exit 1)
	@echo "$(GREEN)✅ Все зависимости найдены$(NC)"

check-env: ## Проверить переменные окружения
	@echo "$(BLUE)🔍 Проверка переменных окружения...$(NC)"
	@test -f .env || (echo "$(YELLOW)⚠️ .env файл не найден, будут использованы значения по умолчанию$(NC)")
	@echo "$(GREEN)✅ Проверка окружения завершена$(NC)"

install: check-deps ## Установить зависимости
	@echo "$(GREEN)📦 Установка зависимостей...$(NC)"
	$(PIP) install -r requirements.txt
	@echo "$(GREEN)✅ Зависимости установлены$(NC)"

setup: install ## Настройка проекта
	@echo "$(GREEN)⚙️ Настройка проекта...$(NC)"
	playwright install
	@echo "$(GREEN)✅ Настройка завершена$(NC)"

# Основные команды тестирования
test-%: check-env ## Универсальная команда для тестирования (test-dev, test-prod)
	@echo "$(GREEN)🧪 Запуск тестов на $(subst test-,,$@)...$(NC)"
	TEST_ENVIRONMENT=$(subst test-,,$@) $(PYTEST) tests/ui/ -sv --browser=chromium --alluredir=reports/allure-results || true

test-head-%: check-env ## Запуск тестов в head режиме (test-head-dev, test-head-prod)
	@echo "$(GREEN)👁️ Запуск тестов в head режиме на $(subst test-head-,,$@)...$(NC)"
	TEST_ENVIRONMENT=$(subst test-head-,,$@) HEADLESS=false $(PYTEST) tests/ui/ -sv --alluredir=reports/allure-results || true

test-ui: ## Запустить все UI тесты
	@echo "$(GREEN)🖥️ Запуск UI тестов...$(NC)"
	$(PYTEST) tests/ui/ -sv --alluredir=reports/allure-results || true

test-api: ## Запустить все API тесты
	@echo "$(GREEN)🔌 Запуск API тестов...$(NC)"
	$(PYTEST) tests/api/ -sv --alluredir=reports/allure-results || true

test-mobile-dev: ## Запустить все мобильные тесты
	@echo "$(GREEN)📱 Запуск мобильных тестов...$(NC)"
	TEST_ENVIRONMENT=dev HEADLESS=false $(PYTEST) tests/ui/mobile/ -sv -m "mobile" --alluredir=reports/allure-results || true
test-mobile-prod: ## Запустить все мобильные тесты
	@echo "$(GREEN)📱 Запуск мобильных тестов...$(NC)"
	TEST_ENVIRONMENT=prod $(PYTEST) tests/ui/mobile/ -sv -m "mobile" --alluredir=reports/allure-results || true


# Регрессионное тестирование
regress-dev: ## Полное регрессионное тестирование на dev (все браузеры + мобильные)
	@echo "$(GREEN)🚀 Запуск полного регрессионного тестирования на DEV...$(NC)"
	@echo "$(YELLOW)🖥️ Тестирование в Chromium...$(NC)"
	TEST_ENVIRONMENT=dev $(PYTEST) tests/ui/ -sv --browser=chromium --alluredir=reports/allure-results || true
	@echo "$(YELLOW)🖥️ Тестирование в Firefox...$(NC)"
	TEST_ENVIRONMENT=dev $(PYTEST) tests/ui/ -sv --browser=firefox --alluredir=reports/allure-results || true
	@echo "$(YELLOW)🖥️ Тестирование в WebKit...$(NC)"
	TEST_ENVIRONMENT=dev $(PYTEST) tests/ui/ -sv --browser=webkit --alluredir=reports/allure-results || true
	@echo "$(YELLOW)📱 Мобильное тестирование на iPhone...$(NC)"
	TEST_ENVIRONMENT=dev $(PYTEST) tests/ui/mobile/ -sv -m "mobile" --alluredir=reports/allure-results || true
	@echo "$(YELLOW)📱 Мобильное тестирование на Android...$(NC)"
	TEST_ENVIRONMENT=dev $(PYTEST) tests/ui/mobile/ -sv --alluredir=reports/allure-results || true
	@echo "$(GREEN)✅ Регрессионное тестирование на DEV завершено!$(NC)"
	@echo "$(YELLOW)📊 Генерация итогового отчета...$(NC)"
	$(ALLURE) generate reports/allure-results -o reports/allure-report --clean || true


regress-prod: ## Полное регрессионное тестирование на prod (все браузеры + мобильные)
	@echo "$(GREEN)🚀 Запуск полного регрессионного тестирования на PROD...$(NC)"
	@echo "$(YELLOW)🖥️ Тестирование в Chromium...$(NC)"
	TEST_ENVIRONMENT=prod $(PYTEST) tests/ui/ -sv --browser=chromium --alluredir=reports/allure-results || true
	@echo "$(YELLOW)🖥️ Тестирование в Firefox...$(NC)"
	TEST_ENVIRONMENT=prod $(PYTEST) tests/ui/ -sv --browser=firefox --alluredir=reports/allure-results || true
	@echo "$(YELLOW)🖥️ Тестирование в WebKit...$(NC)"
	TEST_ENVIRONMENT=prod $(PYTEST) tests/ui/ -sv --browser=webkit --alluredir=reports/allure-results || true
	@echo "$(YELLOW)📱 Мобильное тестирование$(NC)"
	TEST_ENVIRONMENT=prod $(PYTEST) tests/ui/mobile/ -sv -m "mobile" --alluredir=reports/allure-results || true
	@echo "$(GREEN)✅ Регрессионное тестирование на PROD завершено!$(NC)"
	@echo "$(YELLOW)📊 Генерация итогового отчета...$(NC)"
	$(ALLURE) generate reports/allure-results -o reports/allure-report --clean || true


# Отчеты
report: ## Сгенерировать отчет
	@echo "$(GREEN)📊 Генерация отчета...$(NC)"
	$(ALLURE) generate reports/allure-results -o reports/allure-report --clean || true

serve: ## Запустить сервер с отчетом
	@echo "$(GREEN)🌐 Запуск сервера с отчетом...$(NC)"
	@echo "$(YELLOW)📍 Отчет: http://localhost:8080$(NC)"
	$(ALLURE) serve reports/allure-results

# Очистка
clean: ## Очистить временные файлы
	@echo "$(GREEN)🧹 Очистка...$(NC)"
	rm -rf reports/ logs/ .pytest_cache/ __pycache__/
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type d -name "reports" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "allure-results" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "screenshots" -exec rm -rf {} + 2>/dev/null || true

# Форматирование и линтинг
format: ## Отформатировать весь код (Black + isort)
	@echo "$(GREEN)🎨 Форматирование кода...$(NC)"
	$(BLACK) .
	$(ISORT) .
	@echo "$(GREEN)✅ Форматирование завершено!$(NC)"

lint: ## Проверить код линтерами
	@echo "$(GREEN)🔍 Проверка кода линтерами...$(NC)"
	$(FLAKE8) . --count --select=E9,F63,F7,F82 --show-source --statistics
	$(FLAKE8) . --count --exit-zero --max-complexity=10 --max-line-length=88 --statistics
	@echo "$(GREEN)✅ Проверка кода завершена!$(NC)"

format-check: ## Проверить форматирование кода без изменений
	@echo "$(GREEN)🔍 Проверка форматирования кода...$(NC)"
	$(BLACK) . --check
	$(ISORT) . --check-only
	@echo "$(GREEN)✅ Форматирование корректно!$(NC)"