## 🛠️ Быстрый старт

### 1. Установка
```bash
make install
make setup
```

### 2. Настройка окружения
```bash
# Создайте .env файл
PROD_BASE_URL=https://virtualtours.qbd.ae/map
HEADLESS=true
```

### 3. Запуск тестов
```bash
# Все тесты
make test

# UI тесты
make test-ui

# API тесты
make test-api
```

## 🔧 Основные команды

| Команда | Описание |
|---------|----------|
| `make test` | Запустить все тесты |
| `make test-ui` | Запустить UI тесты |
| `make test-api` | Запустить API тесты |
| `make test-head` | Запустить UI тесты в head режиме |
| `make regress-prod` | Полная регрессия на PROD (все браузеры) |
| `make regress-dev` | Полная регрессия на DEV (все браузеры) |
| `make report` | Сгенерировать отчет |
| `make serve` | Запустить сервер с отчетом |
| `make clean` | Очистить временные файлы |

### Ручной запуск через GitHub Actions

#### Способ 1: Через веб-интерфейс
1. Перейти в раздел **Actions** → **Tests CI Pipeline**
2. Нажать **Run workflow**
3. Выбрать параметры:
   - **Branch**: `main` (или другая ветка)
   - **Environment**: `prod` или `dev`
   - **Browsers**: `chromium`, `firefox`, `webkit` или `all`
   - **Run type**: `smoke`, `regression` или `full`
4. Нажать **Run workflow**

#### Способ 2: Быстрые ссылки

##### 🟢 PRODUCTION окружение
[![Run Tests on PROD](https://img.shields.io/badge/Run_Tests_on_PROD-00ff00?style=for-the-badge&logo=github)](https://github.com/username/repo/actions/workflows/cicd.yml?query=event%3Aworkflow_dispatch)

##### 🟡 DEVELOPMENT окружение
[![Run Tests on DEV](https://img.shields.io/badge/Run_Tests_on_DEV-ffff00?style=for-the-badge&logo=github)](https://github.com/username/repo/actions/workflows/cicd.yml?query=event%3Aworkflow_dispatch)

