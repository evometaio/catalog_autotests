# 🚀 Quick Start Guide - Новая Архитектура

## ✅ Что уже есть из коробки

### Компоненты (готовые к использованию):
- `map` - работа с картой и навигацией по проектам
- `amenities` - модальное окно Explore Amenities
- `navigation` - навигация по зданиям/этажам/апартаментам
- `apartment_widget` - виджет 3D апартамента
- `apartment_info` - информация об апартаменте
- `area_tour_360` - 360° тур по территории

### Core функции:
- `browser` - все Playwright действия (click, fill, get_text, etc.)
- `assertions` - проверки (assert_that, assert_url_contains, etc.)

---

## 📝 Примеры использования

### 1. Простой тест для существующего проекта

```python
import allure
import pytest

@allure.feature("Qube - Проект Arisha")
@allure.story("Новая фича")
@pytest.mark.smoke
def test_arisha_new_feature(arisha_page):
    """Описание теста."""
    
    # Открыть и перейти к проекту
    arisha_page.open(route_type="map")
    arisha_page.map.navigate_to_project("arisha")
    
    # Использовать готовые компоненты
    arisha_page.amenities.click_explore_button()
    arisha_page.amenities.verify_modal_displayed()
    
    # Проверки
    arisha_page.assertions.assert_url_contains("/arisha/", "Ошибка навигации")
```

**Время написания: ~3 минуты**

---

### 2. Добавление нового проекта (пример: "Serenity")

#### Шаг 1: Создать локаторы `locators/qube/serenity_locators.py`

```python
from locators.base_locators import BaseLocators

class SerenityLocators(BaseLocators):
    """Локаторы для проекта Serenity."""
    
    # Только уникальные локаторы проекта!
    MAP_LOCATOR_DESKTOP = 'div[aria-label="SERENITY"]'
    MAP_LOCATOR_MOBILE = 'img[alt="Serenity"]'
    
    # Если есть специфичные кнопки:
    # SPECIAL_BUTTON = '[data-test-id="serenity-special-button"]'
```

#### Шаг 2: Создать страницу `pages/projects/qube/serenity_page.py`

```python
from playwright.sync_api import Page
from pages.projects.qube.qube_base_page import QubeBasePage
from locators.qube.serenity_locators import SerenityLocators

class SerenityPage(QubeBasePage):
    """Страница проекта Serenity."""
    
    def __init__(self, page: Page):
        super().__init__(page, SerenityLocators)
    
    # Добавьте методы только для уникальных функций Serenity
    # Всё остальное уже есть в QubeBasePage:
    # - map (навигация)
    # - amenities (удобства)
    # - navigation (здания/этажи)
    # - apartment_widget (виджет)
    # - apartment_info (информация)
    # - area_tour_360 (360 тур)
```

#### Шаг 3: Добавить фикстуру в `conftest.py`

```python
@pytest.fixture
def serenity_page(page: Page):
    """Фикстура для страницы Serenity."""
    from pages.projects.qube.serenity_page import SerenityPage
    return SerenityPage(page)
```

#### Шаг 4: Написать тест

```python
def test_serenity_amenities(serenity_page):
    """Тест Explore Amenities для Serenity."""
    
    serenity_page.open(route_type="map")
    serenity_page.map.navigate_to_project("serenity")
    serenity_page.amenities.click_explore_button()
    serenity_page.amenities.verify_modal_displayed()
    serenity_page.amenities.close_modal()
```

**Время на добавление проекта: ~10-15 минут**

---

### 3. Добавление нового компонента

Если нужна новая функция (например, фильтры):

#### `pages/components/filters_component.py`

```python
import allure
from playwright.sync_api import Page
from pages.core.browser_actions import BrowserActions
from pages.core.assertions import Assertions

class FiltersComponent:
    """Компонент фильтрации."""
    
    def __init__(self, page: Page, locators):
        self.page = page
        self.locators = locators
        self.browser = BrowserActions(page)
        self.assertions = Assertions(page)
    
    @allure.step("Применить фильтр: {filter_name}")
    def apply_filter(self, filter_name: str):
        """Применить фильтр."""
        selector = f'[data-filter="{filter_name}"]'
        self.browser.click(selector)
    
    @allure.step("Проверить примененные фильтры")
    def verify_filters_applied(self):
        """Проверить что фильтры применены."""
        active_filters = self.browser.get_element_count('[data-filter-active="true"]')
        self.assertions.assert_that(active_filters > 0, "Нет активных фильтров")
```

#### Использование в проекте:

```python
class ArishaPage(QubeBasePage):
    def __init__(self, page: Page):
        super().__init__(page, ArishaLocators)
        # Добавляем новый компонент
        self.filters = FiltersComponent(page, self.project_locators)

# В тесте:
def test_filters(arisha_page):
    arisha_page.filters.apply_filter("2-bedroom")
    arisha_page.filters.verify_filters_applied()
```

---

## 🎯 Основные принципы

1. **Компоненты** - переиспользуемая функциональность (amenities, map, navigation)
2. **Страницы проектов** - только уникальная логика проекта
3. **Базовые страницы** (QubeBasePage, etc.) - общая логика для группы проектов
4. **Локаторы** - отдельные файлы, наследуются от BaseLocators

---

## 📊 Доступные методы

### arisha_page (и все Qube проекты)
```python
# Базовые
arisha_page.open(route_type="map")
arisha_page.get_current_url()

# Компоненты
arisha_page.map.navigate_to_project("arisha")
arisha_page.amenities.click_explore_button()
arisha_page.navigation.find_and_click_available_apartment()
arisha_page.apartment_widget.switch_to_2d_mode()
arisha_page.apartment_info.check_apartment_type()
arisha_page.area_tour_360.click_360_button()

# Browser actions
arisha_page.browser.click(selector)
arisha_page.browser.fill(selector, text)
arisha_page.browser.is_visible(selector)

# Assertions
arisha_page.assertions.assert_that(condition, message)
arisha_page.assertions.assert_url_contains(substring, message)
```

---

## ⚡ Быстрые команды

### Запустить все тесты проекта:
```bash
pytest tests/ui/qube/arisha/ -v
```

### Запустить один тест:
```bash
pytest tests/ui/qube/arisha/test_arisha_explore_amenities.py::test_arisha_explore_amenities -v
```

### Headless режим:
```bash
HEADLESS=true pytest tests/ui/qube/arisha/ -v
```

---

## 🔥 Горячие клавиши разработки

1. Написать новый тест → копировать похожий → изменить название и шаги
2. Добавить проект → скопировать структуру Arisha → заменить названия
3. IDE автодополнение → `arisha_page.` + Ctrl+Space = список всех методов

**Время экономии: 80%** 🚀
