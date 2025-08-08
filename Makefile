.PHONY: help install setup test test-ui test-api test-smoke clean report serve-report

# Переменные
PYTHON = python3
PIP = pip3
PYTEST = pytest
ALLURE = allure

# Цвета для вывода
GREEN = \033[0;32m
YELLOW = \033[1;33m
RED = \033[0;31m
NC = \033[0m # No Color

help: ## Показать справку
	@echo "$(GREEN)Доступные команды:$(NC)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(YELLOW)%-20s$(NC) %s\n", $$1, $$2}'

install: ## Установить зависимости
	@echo "$(GREEN)Установка зависимостей...$(NC)"
	$(PIP) install -r requirements.txt

setup: ## Настройка проекта
	@echo "$(GREEN)Настройка проекта...$(NC)"
	$(PIP) install -r requirements.txt
	playwright install

test: ## Запустить все тесты
	@echo "$(GREEN)Запуск всех тестов...$(NC)"
	$(PYTEST) -v --alluredir=reports/allure-results

test-ui: ## Запустить только UI тесты
	@echo "$(GREEN)Запуск UI тестов...$(NC)"
	$(PYTEST) tests/ui/ -v --alluredir=reports/allure-results

test-api: ## Запустить только API тесты
	@echo "$(GREEN)Запуск API тестов...$(NC)"
	$(PYTEST) tests/api/ -v --alluredir=reports/allure-results

test-smoke: ## Запустить дымовые тесты
	@echo "$(GREEN)Запуск дымовых тестов...$(NC)"
	$(PYTEST) -m smoke -v --alluredir=reports/allure-results

report: ## Сгенерировать отчет Allure
	@echo "$(GREEN)Генерация отчета Allure...$(NC)"
	$(ALLURE) generate reports/allure-results -o reports/allure-report --clean

serve-report: ## Запустить локальный сервер с отчетом
	@echo "$(GREEN)Запуск локального сервера с отчетом...$(NC)"
	@echo "$(YELLOW)Отчет будет доступен по адресу: http://localhost:8080$(NC)"
	$(ALLURE) serve reports/allure-results

clean: ## Очистить временные файлы и отчеты
	@echo "$(GREEN)Очистка временных файлов...$(NC)"
	rm -rf reports/
	rm -rf logs/
	rm -rf .pytest_cache/
	rm -rf __pycache__/
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
