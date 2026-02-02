.PHONY: help install setup test clean report mobile

# Переменные
PYTHON = python3
PIP = pip3
PYTEST = pytest
ALLURE = allure

# Цвета
GREEN = \033[0;32m
YELLOW = \033[1;33m
BLUE = \033[0;34m
NC = \033[0m

help: ## Показать справку
	@echo "$(GREEN)🚀 Autotests - Доступные команды:$(NC)"
	@echo "$(BLUE)📱 Мобильное тестирование:$(NC)"
	@grep -E '^mobile-.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(YELLOW)%-25s$(NC) %s\n", $$1, $$2}'
	@echo "$(BLUE)🖥️ Десктопное тестирование:$(NC)"
	@grep -E '^test-.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(YELLOW)%-25s$(NC) %s\n", $$1, $$2}'
	@echo "$(BLUE)📊 Отчеты и утилиты:$(NC)"
	@grep -E '^(report|serve|clean|format|install|setup):.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(YELLOW)%-25s$(NC) %s\n", $$1, $$2}'

install: ## Установить зависимости
	@echo "$(GREEN)📦 Установка зависимостей...$(NC)"
	$(PIP) install -r requirements.txt

setup: ## Настройка проекта
	@echo "$(GREEN)⚙️ Настройка проекта...$(NC)"
	$(PIP) install -r requirements.txt
	playwright install

# ==================== МОБИЛЬНОЕ ТЕСТИРОВАНИЕ ====================


# Мобильные тесты на DEV
mobile-test-dev-iphone: ## Запустить мобильные тесты на iPhone 13 на DEV
	@echo "$(GREEN)📱 Запуск мобильных тестов на iPhone 13 (DEV)...$(NC)"
	MOBILE_DEVICE="iphone_13" TEST_ENVIRONMENT=dev HEADLESS=true $(PYTEST) tests/ui/mobile/ -sv --browser=chromium --alluredir=reports/allure-results || true

mobile-test-dev-iphone-head: ## Запустить мобильные тесты на iPhone 13 в head режиме на DEV
	@echo "$(GREEN)📱 Запуск мобильных тестов на iPhone 13 в head режиме (DEV)...$(NC)"
	MOBILE_DEVICE="iphone_13" TEST_ENVIRONMENT=dev HEADLESS=false $(PYTEST) tests/ui/mobile/ -sv --browser=chromium --alluredir=reports/allure-results || true

mobile-prod-dev-pixel: ## Запустить мобильные тесты на Pixel 5 на DEV
	@echo "$(GREEN)📱 Запуск мобильных тестов на Pixel 5 (DEV)...$(NC)"
	MOBILE_DEVICE="iphone_13" TEST_ENVIRONMENT=prod HEADLESS=true $(PYTEST) tests/ui/mobile/ -sv --browser=chromium --alluredir=reports/allure-results || true


# Мобильная регрессия
mobile-regress-dev: ## Полное мобильное регрессионное тестирование на DEV
	@echo "$(GREEN)📱 Запуск полного мобильного регрессионного тестирования на DEV...$(NC)"
	@echo "$(YELLOW)📱 Тестирование на iPhone 13...$(NC)"
	MOBILE_DEVICE="iphone_13" TEST_ENVIRONMENT=dev $(PYTEST) tests/ui/mobile/ -sv --browser=chromium --alluredir=reports/allure-results || true
	@echo "$(YELLOW)📱 Тестирование на Pixel 5...$(NC)"
	MOBILE_DEVICE="pixel_5" TEST_ENVIRONMENT=dev $(PYTEST) tests/ui/mobile/ -sv --browser=chromium --alluredir=reports/allure-results || true
	@echo "$(GREEN)✅ Мобильное регрессионное тестирование на DEV завершено!$(NC)"

mobile-regress-prod: ## Полное мобильное регрессионное тестирование на PROD
	@echo "$(GREEN)📱 Запуск полного мобильного регрессионного тестирования на PROD...$(NC)"
	@echo "$(YELLOW)📱 Тестирование на iPhone 13...$(NC)"
	MOBILE_DEVICE="iphone_13" TEST_ENVIRONMENT=prod $(PYTEST) tests/ui/mobile/ -sv --browser=chromium --alluredir=reports/allure-results || true
	@echo "$(YELLOW)📱 Тестирование на Pixel 5...$(NC)"
	MOBILE_DEVICE="pixel_5" TEST_ENVIRONMENT=prod $(PYTEST) tests/ui/mobile/ -sv --browser=chromium --alluredir=reports/allure-results || true
	@echo "$(GREEN)✅ Мобильное регрессионное тестирование на PROD завершено!$(NC)"


# ==================== ДЕСКТОПНОЕ ТЕСТИРОВАНИЕ ====================

# Основные команды тестирования
test-dev: ## Запустить все тесты на DEV
	@echo "$(GREEN)🧪 Запуск всех тестов на DEV...$(NC)"
	TEST_ENVIRONMENT=dev HEADLESS=true $(PYTEST) tests/ui/qube/ tests/ui/wellcube/ tests/ui/capstone/ tests/ui/lsr -sv --browser=chromium --alluredir=reports/allure-results || true

test-head-dev: ## Запустить все UI тесты в head режиме на DEV
	@echo "$(GREEN)👁️ Запуск UI тестов в head режиме на DEV...$(NC)"
	TEST_ENVIRONMENT=dev HEADLESS=false $(PYTEST) tests/ui/qube/ tests/ui/wellcube/ tests/ui/capstone/ tests/ui/lsr -sv --alluredir=reports/allure-results || true

test-prod: ## Запустить все тесты на PROD
	@echo "$(GREEN)🧪 Запуск всех тестов на PROD...$(NC)"
	TEST_ENVIRONMENT=prod HEADLESS=true $(PYTEST) tests/ui/qube/ tests/ui/wellcube/ tests/ui/capstone/ tests/ui/lsr  -sv --alluredir=reports/allure-results || true

test-head-prod: ## Запустить все UI тесты в head режиме
	@echo "$(GREEN)👁️ Запуск UI тестов в head режиме на PROD...$(NC)"
	TEST_ENVIRONMENT=prod HEADLESS=false $(PYTEST) tests/ui/qube/ tests/ui/wellcube/ tests/ui/capstone/ tests/ui/lsr -sv --alluredir=reports/allure-results || true

test-ui: ## Запустить все UI тесты
	@echo "$(GREEN)🖥️ Запуск UI тестов...$(NC)"
	HEADLESS=true $(PYTEST) tests/ui/qube/ tests/ui/wellcube/ tests/ui/capstone/ tests/ui/lsr -sv --alluredir=reports/allure-results || true

test-api: ## Запустить все API тесты
	@echo "$(GREEN)🔌 Запуск API тестов...$(NC)"
	$(PYTEST) tests/api/ -sv --alluredir=reports/allure-results || true


# Регрессионное тестирование
regress-dev: ## Полное регрессионное тестирование на dev (все браузеры)
	@echo "$(GREEN)🚀 Запуск полного регрессионного тестирования на DEV...$(NC)"
	@echo "$(YELLOW)🖥️ Тестирование в Chromium...$(NC)"
	TEST_ENVIRONMENT=dev HEADLESS=true $(PYTEST) tests/ui/qube/ tests/ui/wellcube/ tests/ui/capstone/ tests/ui/lsr tests/ui/vibe tests/ui/abra/ tests/ui/msg/ -sv --browser=chromium --alluredir=reports/allure-results || true
	@echo "$(YELLOW)🖥️ Тестирование в Firefox...$(NC)"
	TEST_ENVIRONMENT=dev HEADLESS=true $(PYTEST) tests/ui/qube/ tests/ui/wellcube/ tests/ui/capstone/ tests/ui/lsr tests/ui/vibe tests/ui/abra/ tests/ui/msg/ -sv --browser=firefox --alluredir=reports/allure-results || true
	@echo "$(YELLOW)🖥️ Тестирование в WebKit...$(NC)"
	TEST_ENVIRONMENT=dev HEADLESS=true $(PYTEST) tests/ui/qube/ tests/ui/wellcube/ tests/ui/capstone/ tests/ui/lsr tests/ui/vibe tests/ui/abra/ tests/ui/msg/ -sv --browser=webkit --alluredir=reports/allure-results || true
	@echo "$(GREEN)✅ Тестирование на mobile!$(NC)"
	TEST_ENVIRONMENT=dev HEADLESS=true MOBILE_DEVICE="iphone_13" $(PYTEST) tests/ui/mobile/ -sv --browser=chromium --alluredir=reports/allure-results || true
	@echo "$(GREEN)✅ Регрессионное тестирование на DEV завершено!$(NC)"
	@echo "$(YELLOW)📊 Генерация итогового отчета...$(NC)"
	$(ALLURE) generate reports/allure-results -o reports/allure-report --clean || true


regress-prod: ## Полное регрессионное тестирование на prod (все браузеры)
	@echo "$(GREEN)🚀 Запуск полного регрессионного тестирования на PROD...$(NC)"
	@echo "$(YELLOW)🖥️ Тестирование в Chromium...$(NC)"
	TEST_ENVIRONMENT=prod HEADLESS=true $(PYTEST) tests/ui/qube/ tests/ui/wellcube/ tests/ui/capstone/ tests/ui/vibe tests/ui/lsr tests/ui/abra/ tests/ui/msg/ -sv --browser=chromium --alluredir=reports/allure-results || true
	@echo "$(YELLOW)🖥️ Тестирование в Firefox...$(NC)"
	TEST_ENVIRONMENT=prod HEADLESS=true $(PYTEST) tests/ui/qube/ tests/ui/wellcube/ tests/ui/capstone/ tests/ui/vibe tests/ui/lsr tests/ui/abra/ tests/ui/msg/ -sv --browser=firefox --alluredir=reports/allure-results || true
	@echo "$(YELLOW)🖥️ Тестирование в WebKit...$(NC)"
	TEST_ENVIRONMENT=prod HEADLESS=true $(PYTEST) tests/ui/qube/ tests/ui/wellcube/ tests/ui/capstone/ tests/ui/vibe tests/ui/lsr tests/ui/abra/ tests/ui/msg/ -sv --browser=webkit --alluredir=reports/allure-results || true
	@echo "$(GREEN)✅ Тестирование на mobile!$(NC)"
	TEST_ENVIRONMENT=prod HEADLESS=true MOBILE_DEVICE="iphone_13" $(PYTEST) tests/ui/mobile -sv --browser=chromium --alluredir=reports/allure-results || true
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