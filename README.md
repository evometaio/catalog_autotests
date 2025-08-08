# Autotests Framework


## 🛠 Установка

1. **Клонируйте репозиторий:**
```bash
git clone <repository-url>
cd autotests
```

2. **Создайте виртуальное окружение:**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate     # Windows
```

3. **Установите зависимости:**
```bash
pip install -r requirements.txt
```

4. **Установите браузеры для Playwright:**
```bash
playwright install
```

## 🏃‍♂️ Запуск тестов

### Все тесты
```bash
pytest
```

### Только UI тесты
```bash
pytest tests/ui/
```

### Только API тесты
```bash
pytest tests/api/
```

### С определенными маркерами
```bash
pytest -m smoke
pytest -m regression
```

### Параллельный запуск
```bash
pytest -n auto
```

## 📊 Отчеты

После выполнения тестов отчеты доступны в папке `reports/`:

```bash
# Генерация HTML отчета Allure
allure serve reports/allure-results

# Или создание статического отчета
allure generate reports/allure-results -o reports/allure-report
```

## 🏷 Маркеры тестов

- `@pytest.mark.smoke` - smoke тесты
- `@pytest.mark.regression` - регрессионные тесты


## 🤝 Как работать?

1. Форкните репозиторий
2. Создайте ветку для новой функции
3. Внесите изменения
4. Добавьте тесты
5. Создайте Pull Request
