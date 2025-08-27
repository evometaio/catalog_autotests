# Простой Makefile для autotests
# Только необходимое, без избыточности

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
test: ## Запустить все тесты
	@echo "$(GREEN)🧪 Запуск всех тестов...$(NC)"
	$(PYTEST) -sv --alluredir=reports/allure-results

test-ui: ## Запустить UI тесты
	@echo "$(GREEN)🖥️ Запуск UI тестов...$(NC)"
	$(PYTEST) tests/ui/ -sv --alluredir=reports/allure-results

test-api: ## Запустить API тесты
	@echo "$(GREEN)🔌 Запуск API тестов...$(NC)"
	$(PYTEST) tests/api/ -sv --alluredir=reports/allure-results



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