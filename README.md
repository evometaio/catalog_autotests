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
| `make report` | Сгенерировать отчет |
| `make clean` | Очистить временные файлы |



