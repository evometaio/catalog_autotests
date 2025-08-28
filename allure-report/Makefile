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
	@echo "$(GREEN)🧪 Запуск всех тестов...$(NC)"
	$(PYTEST) tests/ui/ -sv --environment=dev --browser=chromium --alluredir=reports/allure-results || true

test-prod: ## Запустить все тесты на PROD
	@echo "$(GREEN)🧪 Запуск всех тестов...$(NC)"
	$(PYTEST) -sv --alluredir=reports/allure-results || true

test-ui: ## Запустить все UI тесты
	@echo "$(GREEN)🖥️ Запуск UI тестов...$(NC)"
	$(PYTEST) tests/ui/ -sv --alluredir=reports/allure-results || true

test-api: ## Запустить все API тесты
	@echo "$(GREEN)🔌 Запуск API тестов...$(NC)"
	$(PYTEST) tests/api/ -sv --alluredir=reports/allure-results || true

test-head: ## Запустить все UI тесты в head режиме
	@echo "$(GREEN)👁️ Запуск UI тестов в head режиме...$(NC)"
	HEADLESS=false $(PYTEST) tests/ui/ -sv --alluredir=reports/allure-results || true

# Регрессионное тестирование
regress-prod: ## Полное регрессионное тестирование на prod (все браузеры)
	@echo "$(GREEN)🚀 Запуск полного регрессионного тестирования на PROD...$(NC)"
	@echo "$(YELLOW)🖥️ Тестирование в Chromium...$(NC)"
	$(PYTEST) tests/ui/ -sv --browser=chromium --alluredir=reports/allure-results || true
#	@echo "$(YELLOW)🖥️ Тестирование в Firefox...$(NC)"
#	HEADLESS=false $(PYTEST) tests/ui/ -sv --browser=firefox --alluredir=reports/allure-results || true
	@echo "$(YELLOW)🖥️ Тестирование в WebKit...$(NC)"
	$(PYTEST) tests/ui/ -sv --browser=webkit --alluredir=reports/allure-results || true
	@echo "$(GREEN)✅ Регрессионное тестирование на PROD завершено!$(NC)"
	@echo "$(YELLOW)📊 Генерация итогового отчета...$(NC)"
	$(ALLURE) generate reports/allure-results -o reports/allure-report --clean || true

regress-dev: ## Полное регрессионное тестирование на dev (все браузеры)
	@echo "$(GREEN)🚀 Запуск полного регрессионного тестирования на DEV...$(NC)"
	@echo "$(YELLOW)🖥️ Тестирование в Chromium...$(NC)"
	$(PYTEST) tests/ui/ -sv --environment=dev --browser=chromium --alluredir=reports/allure-results || true
#	@echo "$(YELLOW)🖥️ Тестирование в Firefox...$(NC)"
#	$(PYTEST) tests/ui/ -sv --environment=dev --browser=firefox --alluredir=reports/allure-results || true
	@echo "$(YELLOW)🖥️ Тестирование в WebKit...$(NC)"
	$(PYTEST) tests/ui/ -sv --environment=dev --browser=webkit --alluredir=reports/allure-results || true
	@echo "$(GREEN)✅ Регрессионное тестирование на DEV завершено!$(NC)"
	@echo "$(YELLOW)📊 Генерация итогового отчета...$(NC)"
	$(ALLURE) generate reports/allure-results -o reports/allure-report --clean || true

# Отчеты
report: ## Сгенерировать отчет
	@echo "$(GREEN)📊 Генерация отчета...$(NC)"
	$(ALLURE) generate reports/allure-results -o reports/allure-report --clean

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