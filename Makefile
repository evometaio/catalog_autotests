.PHONY: help install setup test clean report

# Переменные
PYTHON = python3
PIP = pip3
PYTEST = pytest
ALLURE = allure

# Цвета
GREEN = \033[0;32m
YELLOW = \033[1;33m
NC = \033[0m

help: ## Показать справку
	@echo "$(GREEN)🚀 Autotests - Доступные команды:$(NC)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(YELLOW)%-20s$(NC) %s\n", $$1, $$2}'

install: ## Установить зависимости
	@echo "$(GREEN)📦 Установка зависимостей...$(NC)"
	$(PIP) install -r requirements.txt

setup: ## Настройка проекта
	@echo "$(GREEN)⚙️ Настройка проекта...$(NC)"
	$(PIP) install -r requirements.txt
	playwright install

# Основные команды тестирования
test-dev: ## Запустить все тесты на DEV
	@echo "$(GREEN)🧪 Запуск всех тестов на DEV...$(NC)"
	TEST_ENVIRONMENT=dev $(PYTEST) tests/ui/ -sv --browser=chromium --alluredir=reports/allure-results || true

test-head-dev: ## Запустить все UI тесты в head режиме на DEV
	@echo "$(GREEN)👁️ Запуск UI тестов в head режиме на DEV...$(NC)"
	TEST_ENVIRONMENT=dev HEADLESS=false $(PYTEST) tests/ui/ -sv --alluredir=reports/allure-results || true

test-prod: ## Запустить все тесты на PROD
	@echo "$(GREEN)🧪 Запуск всех тестов на PROD...$(NC)"
	TEST_ENVIRONMENT=prod $(PYTEST) tests/ui/ -sv --alluredir=reports/allure-results || true

test-head-prod: ## Запустить все UI тесты в head режиме
	@echo "$(GREEN)👁️ Запуск UI тестов в head режиме на PROD...$(NC)"
	TEST_ENVIRONMENT=prod HEADLESS=false $(PYTEST) tests/ui/ -sv --alluredir=reports/allure-results || true

test-ui: ## Запустить все UI тесты
	@echo "$(GREEN)🖥️ Запуск UI тестов...$(NC)"
	$(PYTEST) tests/ui/ -sv --alluredir=reports/allure-results || true

test-api: ## Запустить все API тесты
	@echo "$(GREEN)🔌 Запуск API тестов...$(NC)"
	$(PYTEST) tests/api/ -sv --alluredir=reports/allure-results || true

test-mobile: ## Запустить все мобильные тесты
	@echo "$(GREEN)📱 Запуск мобильных тестов...$(NC)"
	$(PYTEST) tests/ui/mobile/ -sv --alluredir=reports/allure-results || true

test-mobile-iphone: ## Запустить мобильные тесты на iPhone
	@echo "$(GREEN)📱 Запуск мобильных тестов на iPhone...$(NC)"
	$(PYTEST) tests/ui/mobile/ -sv -m "mobile_device('iPhone 13 Pro')" --alluredir=reports/allure-results || true

test-mobile-android: ## Запустить мобильные тесты на Android
	@echo "$(GREEN)📱 Запуск мобильных тестов на Android...$(NC)"
	$(PYTEST) tests/ui/mobile/ -sv -m "mobile_device('Pixel 5')" --alluredir=reports/allure-results || true

test-responsive: ## Запустить тесты адаптивности (desktop + mobile)
	@echo "$(GREEN)📱💻 Запуск тестов адаптивности...$(NC)"
	$(PYTEST) tests/ui/ -sv -m "ui" --alluredir=reports/allure-results || true


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
	TEST_ENVIRONMENT=dev $(PYTEST) tests/ui/mobile/ -sv -m "mobile_device('iPhone 13 Pro')" --alluredir=reports/allure-results || true
	@echo "$(YELLOW)📱 Мобильное тестирование на Android...$(NC)"
	TEST_ENVIRONMENT=dev $(PYTEST) tests/ui/mobile/ -sv -m "mobile_device('Pixel 5')" --alluredir=reports/allure-results || true
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
	@echo "$(YELLOW)📱 Мобильное тестирование на iPhone...$(NC)"
	TEST_ENVIRONMENT=prod $(PYTEST) tests/ui/mobile/ -sv -m "mobile_device('iPhone 13 Pro')" --alluredir=reports/allure-results || true
	@echo "$(YELLOW)📱 Мобильное тестирование на Android...$(NC)"
	TEST_ENVIRONMENT=prod $(PYTEST) tests/ui/mobile/ -sv -m "mobile_device('Pixel 5')" --alluredir=reports/allure-results || true
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

# Форматирование кода
format: ## Отформатировать весь код (Black + isort)
	@echo "$(GREEN)🎨 Форматирование кода...$(NC)"
	black .
	isort .
	@echo "$(GREEN)✅ Форматирование завершено!$(NC)"