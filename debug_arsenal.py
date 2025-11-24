"""
Отладочный скрипт для поиска локаторов и проверки флоу для проекта Arsenal.
Запуск: python debug_arsenal.py
"""

import os
import time

from playwright.sync_api import sync_playwright

# Настройки
TEST_ENVIRONMENT = os.getenv("TEST_ENVIRONMENT", "dev")
HEADLESS = os.getenv("HEADLESS", "false").lower() == "true"
MOBILE_DEVICE = os.getenv("MOBILE_DEVICE", "desktop")

# URL-ы
URLS = {
    "dev": "https://catalog-dev.evometa.io/arsenal-east/map",
    "prod": "https://catalog.evometa.io/arsenal-east/map",
}

BASE_URL = URLS.get(TEST_ENVIRONMENT, URLS["dev"])

print(f"🔍 Отладка Arsenal")
print(f"📍 URL: {BASE_URL}")
print(f"📱 Устройство: {MOBILE_DEVICE}")
print(f"👁️ Headless: {HEADLESS}")
print("-" * 80)


def debug_desktop():
    """Отладка desktop версии."""
    print("\n🖥️ === DESKTOP ОТЛАДКА ===\n")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=HEADLESS)
        context = browser.new_context(
            viewport={"width": 1920, "height": 1080},
            ignore_https_errors=True,
        )
        page = context.new_page()

        print(f"1️⃣ Открываем страницу: {BASE_URL}")
        page.goto(BASE_URL)
        page.wait_for_load_state("networkidle")
        time.sleep(3)

        print(f"   Текущий URL: {page.url}")
        print(f"   Заголовок страницы: {page.title()}")

        # Выводим все data-test-id на странице
        print("\n2️⃣ Все элементы с data-test-id:")
        test_ids = page.locator("[data-test-id]").all()
        test_id_values = set()
        for el in test_ids[:50]:  # Ограничиваем до 50 для читаемости
            try:
                test_id = el.get_attribute("data-test-id")
                if test_id:
                    test_id_values.add(test_id)
            except:
                pass

        for test_id in sorted(test_id_values):
            count = page.locator(f'[data-test-id="{test_id}"]').count()
            print(f"   - {test_id}: {count} элементов")

        print("\n3️⃣ Ищем элементы навигации:")

        # Ищем кнопку All Units
        all_units_selectors = [
            '[data-test-id="nav-desktop-catalog2d-standalone"]',
            '[data-test-id="nav-desktop-catalog2d"]',
            '[data-test-id*="catalog"]',
            '[data-test-id*="Catalog"]',
            'button:has-text("All Units")',
            'button:has-text("All units")',
            'a:has-text("All Units")',
            'button:has-text("Все квартиры")',
            'a:has-text("Все квартиры")',
        ]

        for selector in all_units_selectors:
            elements = page.locator(selector)
            count = elements.count()
            if count > 0:
                print(f"   ✅ Найдено '{selector}': {count} элементов")
                for i in range(min(count, 3)):
                    try:
                        el = elements.nth(i)
                        if el.is_visible():
                            print(
                                f"      - Элемент #{i}: видимый, текст: '{el.text_content()[:50]}'"
                            )
                    except:
                        pass
            else:
                print(f"   ❌ Не найдено: '{selector}'")

        # Ищем кнопку 360 Area Tour на главной странице
        print("\n5️⃣ Ищем кнопку 360 Area Tour на главной странице:")
        area_tour_selectors = [
            '[data-test-id="nav-rotation-view-controls-button"]',
            'button:has-text("360")',
            'button:has-text("Панорамы")',
            '[aria-label*="360"]',
            '[aria-label*="panorama"]',
        ]

        for selector in area_tour_selectors:
            elements = page.locator(selector)
            count = elements.count()
            if count > 0:
                print(f"   ✅ Найдено '{selector}': {count} элементов")
                for i in range(min(count, 3)):
                    try:
                        el = elements.nth(i)
                        if el.is_visible():
                            print(f"      - Элемент #{i}: видимый")
                    except:
                        pass

        # Переходим в каталог и ищем кнопку 360 там
        print("\n5.1️⃣ Переходим в каталог и ищем кнопку 360 Area Tour:")
        project_button = page.locator('[data-test-id="nav-desktop-project-vibe"]')
        if project_button.count() > 0:
            try:
                project_button.first.click()
                page.wait_for_timeout(3000)
                print(f"   ✅ Перешли в каталог, URL: {page.url}")

                # Ищем кнопку 360 на странице каталога
                for selector in area_tour_selectors:
                    elements = page.locator(selector)
                    count = elements.count()
                    if count > 0:
                        print(
                            f"   ✅ На странице каталога найдено '{selector}': {count} элементов"
                        )
                        for i in range(min(count, 3)):
                            try:
                                el = elements.nth(i)
                                if el.is_visible():
                                    print(f"      - Элемент #{i}: видимый")
                            except:
                                pass
            except Exception as e:
                print(f"   ❌ Ошибка при переходе в каталог: {e}")

        map_selectors = [
            'div[aria-label*="ARSENAL"]',
            'div[aria-label*="Arsenal"]',
            'div[aria-label*="arsenal"]',
            '[data-test-id*="arsenal"]',
            '[data-test-id*="Arsenal"]',
        ]

        for selector in map_selectors:
            elements = page.locator(selector)
            count = elements.count()
            if count > 0:
                print(f"   ✅ Найдено '{selector}': {count} элементов")

        # Проверяем наличие каталога
        print("\n6️⃣ Проверяем наличие элементов каталога на текущей странице:")
        catalog_selectors = [
            '[data-test-id^="property-info-primary-button-"]',
            '[data-test-id^="property-info-secondary-button-"]',
            'button:has-text("VIEW APARTMENT")',
        ]

        for selector in catalog_selectors:
            elements = page.locator(selector)
            count = elements.count()
            if count > 0:
                print(f"   ✅ Найдено '{selector}': {count} элементов")

        # Пробуем кликнуть на проект
        print("\n7️⃣ Пробуем кликнуть на проект Arsenal:")
        project_button = page.locator('[data-test-id="nav-desktop-project-vibe"]')
        if project_button.count() > 0:
            try:
                print(f"   Найдена кнопка проекта, кликаем...")
                project_button.first.click()
                page.wait_for_timeout(3000)
                current_url = page.url
                print(f"   ✅ Кликнули, текущий URL: {current_url}")

                # Ищем новые элементы после клика
                print("\n8️⃣ Ищем элементы после клика на проект:")
                new_test_ids = page.locator("[data-test-id]").all()
                new_test_id_values = set()
                for el in new_test_ids[:50]:
                    try:
                        test_id = el.get_attribute("data-test-id")
                        if test_id:
                            new_test_id_values.add(test_id)
                    except:
                        pass

                for test_id in sorted(new_test_id_values):
                    if test_id not in test_id_values:
                        count = page.locator(f'[data-test-id="{test_id}"]').count()
                        print(f"   - НОВЫЙ: {test_id}: {count} элементов")

                # Ищем кнопку каталога
                print("\n9️⃣ Ищем кнопку каталога после клика на проект:")
                catalog_after_click = [
                    '[data-test-id*="catalog"]',
                    '[data-test-id*="Catalog"]',
                    'button:has-text("All Units")',
                    'button:has-text("All units")',
                    'a:has-text("All Units")',
                ]

                for selector in catalog_after_click:
                    elements = page.locator(selector)
                    count = elements.count()
                    if count > 0:
                        print(f"   ✅ Найдено '{selector}': {count} элементов")
                        try:
                            elements.first.click()
                            page.wait_for_timeout(3000)
                            print(f"   ✅ Кликнули на каталог, URL: {page.url}")

                            # Проверяем элементы каталога
                            print("\n🔟 Элементы каталога:")
                            property_buttons = page.locator(
                                '[data-test-id^="property-info-primary-button-"]'
                            )
                            count = property_buttons.count()
                            print(f"   Кнопок квартир: {count}")
                            if count > 0:
                                for i in range(min(count, 3)):
                                    try:
                                        btn = property_buttons.nth(i)
                                        text = btn.text_content()
                                        print(f"      - Кнопка #{i}: '{text[:50]}'")
                                    except:
                                        pass
                        except Exception as e:
                            print(f"   ❌ Ошибка: {e}")
            except Exception as e:
                print(f"   ❌ Ошибка при клике на проект: {e}")
        else:
            print("   ❌ Кнопка проекта не найдена")

        if not HEADLESS:
            print("\n⏸️ Ожидание 10 секунд для ручной проверки...")
            time.sleep(10)

        browser.close()


def debug_mobile():
    """Отладка mobile версии."""
    print("\n📱 === MOBILE ОТЛАДКА ===\n")

    mobile_config = {
        "iphone_13": {
            "viewport": {"width": 390, "height": 844},
            "device_scale_factor": 3,
            "is_mobile": True,
            "has_touch": True,
            "user_agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
        },
        "pixel_5": {
            "viewport": {"width": 393, "height": 851},
            "device_scale_factor": 2.75,
            "is_mobile": True,
            "has_touch": True,
            "user_agent": "Mozilla/5.0 (Linux; Android 11; Pixel 5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36",
        },
    }

    device_config = mobile_config.get(MOBILE_DEVICE, mobile_config["iphone_13"])

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=HEADLESS)
        context = browser.new_context(
            viewport=device_config["viewport"],
            device_scale_factor=device_config["device_scale_factor"],
            is_mobile=device_config["is_mobile"],
            has_touch=device_config["has_touch"],
            user_agent=device_config["user_agent"],
            ignore_https_errors=True,
        )
        page = context.new_page()

        print(f"1️⃣ Открываем страницу: {BASE_URL}")
        page.goto(BASE_URL)
        page.wait_for_load_state("networkidle")
        time.sleep(3)

        print(f"   Текущий URL: {page.url}")
        print(f"   Заголовок страницы: {page.title()}")

        # Выводим все data-test-id на странице
        print("\n2️⃣ Все элементы с data-test-id (первые 30):")
        test_ids = page.locator("[data-test-id]").all()
        test_id_values = set()
        for el in test_ids[:30]:
            try:
                test_id = el.get_attribute("data-test-id")
                if test_id:
                    test_id_values.add(test_id)
            except:
                pass

        for test_id in sorted(test_id_values):
            count = page.locator(f'[data-test-id="{test_id}"]').count()
            print(f"   - {test_id}: {count} элементов")

        print("\n3️⃣ Ищем кнопку входа в проект:")
        project_button_selectors = [
            '[data-test-id="nav-desktop-project-vibe"]',
            '[data-test-id*="project"]',
            '[data-test-id*="Project"]',
            'button:has-text("Arsenal")',
            'button:has-text("ARSENAL")',
            'a:has-text("Arsenal")',
        ]

        project_button_found = False
        for selector in project_button_selectors:
            elements = page.locator(selector)
            count = elements.count()
            if count > 0:
                print(f"   ✅ Найдено '{selector}': {count} элементов")
                for i in range(min(count, 3)):
                    try:
                        el = elements.nth(i)
                        text = el.text_content() or el.get_attribute("aria-label") or ""
                        is_visible = el.is_visible()
                        print(
                            f"      - Элемент #{i}: видимый={is_visible}, текст='{text[:50]}'"
                        )
                        if is_visible and not project_button_found:
                            project_button_found = True
                            print(f"      🎯 Пробуем кликнуть на элемент #{i}...")
                            el.click()
                            page.wait_for_timeout(3000)
                            new_url = page.url
                            print(f"      ✅ Кликнули! Новый URL: {new_url}")

                            # Проверяем новые элементы после клика
                            print("\n4️⃣ Элементы после клика на проект:")
                            new_test_ids = page.locator("[data-test-id]").all()
                            new_test_id_values = set()
                            for el in new_test_ids[:30]:
                                try:
                                    test_id = el.get_attribute("data-test-id")
                                    if test_id:
                                        new_test_id_values.add(test_id)
                                except:
                                    pass

                            for test_id in sorted(new_test_id_values):
                                count = page.locator(
                                    f'[data-test-id="{test_id}"]'
                                ).count()
                                print(f"   - {test_id}: {count} элементов")
                            break
                    except Exception as e:
                        print(f"      ❌ Ошибка: {e}")

        print("\n5️⃣ Ищем проект Vibe на карте (по aria-label и title):")
        vibe_map_selectors = [
            'div[aria-label="Vibe"]',
            'div[title="Vibe"]',
            'div[role="img"][aria-label="Vibe"]',
            'div[role="img"][title="Vibe"]',
        ]

        vibe_clicked = False
        for selector in vibe_map_selectors:
            elements = page.locator(selector)
            count = elements.count()
            if count > 0:
                print(f"   ✅ Найдено '{selector}': {count} элементов")
                for i in range(min(count, 5)):
                    try:
                        el = elements.nth(i)
                        aria_label = el.get_attribute("aria-label") or ""
                        title = el.get_attribute("title") or ""
                        role = el.get_attribute("role") or ""
                        is_visible = el.is_visible()
                        print(
                            f"      - Элемент #{i}: видимый={is_visible}, aria-label='{aria_label}', title='{title}', role='{role}'"
                        )
                        if ("Vibe" in (aria_label + title)) and not vibe_clicked:
                            print(f"      🎯 Пробуем кликнуть на Vibe элемент #{i}...")
                            el.click()
                            page.wait_for_timeout(3000)
                            new_url = page.url
                            print(f"      ✅ Кликнули! Новый URL: {new_url}")
                            vibe_clicked = True

                            # Проверяем новые элементы после клика
                            print("\n6️⃣ Элементы после клика на Vibe:")
                            new_test_ids = page.locator("[data-test-id]").all()
                            new_test_id_values = set()
                            for el in new_test_ids[:30]:
                                try:
                                    test_id = el.get_attribute("data-test-id")
                                    if test_id:
                                        new_test_id_values.add(test_id)
                                except:
                                    pass

                            for test_id in sorted(new_test_id_values):
                                count = page.locator(
                                    f'[data-test-id="{test_id}"]'
                                ).count()
                                print(f"   - {test_id}: {count} элементов")

                            # Ищем кнопку Explore Project
                            print(
                                "\n7️⃣ Ищем кнопку Explore Project после клика на Vibe:"
                            )
                            explore_selectors = [
                                '//span[text()="Explore Project"]',
                                'button:has-text("Explore Project")',
                                'a:has-text("Explore Project")',
                            ]

                            for selector in explore_selectors:
                                elements = page.locator(selector)
                                count = elements.count()
                                if count > 0:
                                    print(
                                        f"   ✅ Найдено '{selector}': {count} элементов"
                                    )
                                    try:
                                        elements.first.click()
                                        page.wait_for_timeout(3000)
                                        print(
                                            f"   ✅ Кликнули на Explore Project, URL: {page.url}"
                                        )
                                    except Exception as e:
                                        print(f"   ❌ Ошибка: {e}")
                            break
                    except Exception as e:
                        print(f"      ❌ Ошибка: {e}")

        print("\n8️⃣ Ищем модальное окно проекта:")
        modal_selectors = [
            "div.ant-modal",
            '[role="dialog"]',
            ".ant-modal-content",
        ]

        for selector in modal_selectors:
            elements = page.locator(selector)
            count = elements.count()
            if count > 0:
                print(f"   ✅ Найдено модальное окно '{selector}': {count} элементов")

        explore_selectors = [
            '//span[text()="Explore Project"]',
            'button:has-text("Explore Project")',
            'a:has-text("Explore Project")',
        ]

        for selector in explore_selectors:
            elements = page.locator(selector)
            count = elements.count()
            if count > 0:
                print(f"   ✅ Найдено '{selector}': {count} элементов")
                try:
                    elements.first.click()
                    page.wait_for_timeout(3000)
                    current_url = page.url
                    print(f"   ✅ Кликнули, текущий URL: {current_url}")
                except Exception as e:
                    print(f"   ❌ Ошибка при клике: {e}")

        print("\n5️⃣ Ищем мобильное меню:")
        menu_selectors = [
            '[data-test-id="nav-mobile-menu-toggle"]',
            'button[aria-label*="menu"]',
            'button[aria-label*="Menu"]',
            ".hamburger",
        ]

        for selector in menu_selectors:
            elements = page.locator(selector)
            count = elements.count()
            if count > 0:
                print(f"   ✅ Найдено '{selector}': {count} элементов")

        print("\n6️⃣ Ищем кнопку каталога в мобильном меню:")
        catalog_selectors = [
            '[data-test-id="nav-mobile-catalog2d"]',
            'button:has-text("All Units")',
            'button:has-text("All units")',
            'a:has-text("All Units")',
            'button:has-text("arsenal")',
            'button:has-text("Arsenal")',
        ]

        for selector in catalog_selectors:
            elements = page.locator(selector)
            count = elements.count()
            if count > 0:
                print(f"   ✅ Найдено '{selector}': {count} элементов")

        print("\n7️⃣ Ищем кнопку 360 Area Tour на мобильном:")
        area_tour_selectors = [
            '[data-test-id="nav-rotation-view-controls-button"]',
            'button:has-text("360")',
            'button:has-text("Панорамы")',
        ]

        for selector in area_tour_selectors:
            elements = page.locator(selector)
            count = elements.count()
            if count > 0:
                print(f"   ✅ Найдено '{selector}': {count} элементов")
                for i in range(min(count, 3)):
                    try:
                        el = elements.nth(i)
                        if el.is_visible():
                            print(f"      - Элемент #{i}: видимый")
                    except:
                        pass

        if not HEADLESS:
            print("\n⏸️ Ожидание 10 секунд для ручной проверки...")
            time.sleep(10)

        browser.close()


if __name__ == "__main__":
    print("=" * 80)
    print("🔍 ОТЛАДОЧНЫЙ СКРИПТ ДЛЯ ARSENAL")
    print("=" * 80)

    if MOBILE_DEVICE != "desktop":
        debug_mobile()
    else:
        debug_desktop()

    print("\n" + "=" * 80)
    print("✅ Отладка завершена!")
    print("=" * 80)
