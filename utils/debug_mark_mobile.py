"""Отладочный скрипт для поиска мобильных локаторов проекта MARK (LSR).

Запуск:

    TEST_ENVIRONMENT=dev HEADLESS=false MOBILE_DEVICE="iphone_13" python3 utils/debug_mark_mobile.py

Можно передать свой URL через переменную окружения DEBUG_URL.
"""

import os

from playwright.sync_api import sync_playwright


def _get_mobile_device_config(device_name: str = "iphone_13") -> dict:
    """Простейшая конфигурация мобильных устройств (копия из conftest)."""
    devices = {
        "iphone_13": {
            "viewport": {"width": 390, "height": 844},
            "device_scale_factor": 3,
            "is_mobile": True,
            "has_touch": True,
            "user_agent": (
                "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) "
                "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 "
                "Mobile/15E148 Safari/604.1"
            ),
        },
        "pixel_5": {
            "viewport": {"width": 393, "height": 851},
            "device_scale_factor": 2.75,
            "is_mobile": True,
            "has_touch": True,
            "user_agent": (
                "Mozilla/5.0 (Linux; Android 11; Pixel 5) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/91.0.4472.120 Mobile Safari/537.36"
            ),
        },
    }
    return devices.get(device_name, devices["iphone_13"])


def print_elements(page, selector: str, title: str):
    """Утилита для печати найденных элементов."""
    print("\n" + "=" * 80)
    print(f"🔍 {title} — селектор: {selector}")
    elements = page.locator(selector)
    count = elements.count()
    print(f"Всего элементов: {count}")
    for i in range(count):
        el = elements.nth(i)
        visible = el.is_visible()
        classes = el.get_attribute("class") or ""
        text = (el.text_content() or "").strip()
        print(f"  [{i}] visible={visible} class='{classes}' text='{text[:80]}'")


def debug_mark_mobile():
    """Основная логика отладки мобильных локаторов MARK."""
    env = os.getenv("TEST_ENVIRONMENT", "dev")

    # URL MARK
    default_url = "https://catalog-ru-dev.evometa.io/lsr/project/mark/area"
    url = os.getenv("DEBUG_URL", default_url)

    # Мобильное устройство
    device_name = os.getenv("MOBILE_DEVICE", "iphone_13")
    device_cfg = _get_mobile_device_config(device_name)

    headless = os.getenv("HEADLESS", "false").lower() == "true"

    print("🚀 Отладка мобильной версии MARK")
    print(f"ENV={env}, DEVICE={device_name}, HEADLESS={headless}")
    print(f"URL: {url}")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        context = browser.new_context(
            viewport=device_cfg["viewport"],
            device_scale_factor=device_cfg["device_scale_factor"],
            is_mobile=device_cfg["is_mobile"],
            has_touch=device_cfg["has_touch"],
            user_agent=device_cfg["user_agent"],
        )
        page = context.new_page()

        page.goto(url, wait_until="networkidle")
        page.wait_for_timeout(3000)
        print(f"Текущий URL после загрузки: {page.url}")

        # 1. Навигация / мобильное меню
        print_elements(
            page,
            '[data-test-id^="nav-mobile-"]',
            "Мобильные элементы навигации (nav-mobile-*)",
        )

        # Пробуем открыть мобильное меню и напечатать элементы внутри
        try:
            menu_toggle = page.locator('[data-test-id="nav-mobile-menu-toggle"]')
            if menu_toggle.count() > 0 and menu_toggle.first.is_visible():
                print("\n🔘 Кликаем по nav-mobile-menu-toggle...")
                menu_toggle.first.click()
                page.wait_for_timeout(1000)
                print_elements(
                    page,
                    '[data-test-id^="nav-mobile-"]',
                    "Мобильные элементы навигации после клика по меню",
                )
        except Exception as e:
            print(f"⚠️ Ошибка при клике по мобильному меню: {e}")

        # 2. Кнопка 360 Area Tour
        print_elements(
            page,
            '[data-test-id="nav-rotation-view-controls-button"]',
            "Кнопки Панорамы / 360 (nav-rotation-view-controls-button)",
        )

        # 3. Все data-test-id (для быстрого просмотра структуры)
        print_elements(page, "[data-test-id]", "Все элементы с data-test-id")

        # 4. Скриншот для визуальной проверки
        os.makedirs("reports", exist_ok=True)
        screenshot_path = os.path.join("reports", "mark_mobile_debug.png")
        page.screenshot(path=screenshot_path, full_page=True)
        print(f"\n📸 Скриншот сохранен в: {screenshot_path}")

        browser.close()

    print("\n✅ Отладка мобильных локаторов завершена")


if __name__ == "__main__":
    debug_mark_mobile()


