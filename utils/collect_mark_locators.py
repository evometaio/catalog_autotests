"""Скрипт для сбора локаторов проекта MARK (LSR) на всех ключевых страницах.

Что делает:
- открывает страницу area проекта MARK;
- собирает все data-test-id и основные кнопки;
- переходит в каталог (All units) и снова собирает локаторы;
- кликает по первой доступной квартире, переходит на страницу apartment и собирает локаторы там;
- складывает всё в один JSON-файл reports/mark_all_locators.json.

Запуск (DESKTOP):
    TEST_ENVIRONMENT=dev HEADLESS=true python3 utils/collect_mark_locators.py

Запуск (MOBILE):
    TEST_ENVIRONMENT=dev HEADLESS=false MOBILE_DEVICE="iphone_13" python3 utils/collect_mark_locators.py
"""

import json
import os
from typing import Dict, List

from playwright.sync_api import Page, sync_playwright


def _get_mobile_device_config(device_name: str = "iphone_13") -> dict:
    """Мини-конфигурация мобильных устройств (копия логики из conftest)."""
    return {
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
    }.get(device_name, _get_mobile_device_config.__defaults__[0])  # type: ignore


def collect_page_locators(page: Page, name: str) -> Dict:
    """Собрать базовый набор локаторов с одной страницы."""
    print(f"\n=== Сбор локаторов для страницы: {name} ===")
    data: Dict[str, List[Dict]] = {
        "data_test_ids": [],
        "buttons": [],
        "links": [],
    }

    # Все data-test-id
    elems = page.locator("[data-test-id]").all()
    print(f"  data-test-id элементов: {len(elems)}")
    for el in elems:
        test_id = el.get_attribute("data-test-id") or ""
        tag = el.evaluate("el => el.tagName.toLowerCase()")
        text = (el.text_content() or "").strip()
        data["data_test_ids"].append(
            {
                "test_id": test_id,
                "tag": tag,
                "text": text[:120],
            }
        )

    # Кнопки
    buttons = page.locator("button").all()
    print(f"  кнопок: {len(buttons)}")
    for btn in buttons:
        text = (btn.text_content() or "").strip()
        test_id = btn.get_attribute("data-test-id") or ""
        classes = btn.get_attribute("class") or ""
        data["buttons"].append(
            {
                "text": text[:120],
                "data_test_id": test_id,
                "classes": classes[:160],
            }
        )

    # Ссылки
    links = page.locator("a[href]").all()
    print(f"  ссылок: {len(links)}")
    for a in links:
        text = (a.text_content() or "").strip()
        href = a.get_attribute("href") or ""
        data["links"].append(
            {
                "text": text[:120],
                "href": href,
            }
        )

    return data


def open_mark_area_url(page: Page) -> str:
    """Открыть базовый URL MARK (area) на основе TEST_ENVIRONMENT.

    Здесь нельзя импортировать pytest-конфигурацию как модуль (conftest),
    поэтому читаем URL из окружения так же, как это делает conftest._get_urls_by_environment.
    """
    env = os.getenv("TEST_ENVIRONMENT", "dev")
    if env == "dev":
        url = os.getenv(
            "DEV_LSR_MARK_BASE_URL",
            "https://catalog-ru-dev.evometa.io/lsr/project/mark/area",
        )
    else:
        url = os.getenv(
            "LSR_MARK_PROD_BASE_URL",
            "https://catalog-ru.evometa.io/lsr/project/mark/area",
        )
    print(f"\n➡️ Открываем MARK area: {url}")
    page.goto(url, wait_until="networkidle")
    page.wait_for_timeout(2000)
    print(f"Текущий URL: {page.url}")
    return page.url


def navigate_to_catalog(page: Page, is_mobile: bool):
    """Перейти на страницу каталога MARK."""
    if is_mobile:
        print("\n➡️ MOBILE: открываем меню и кликаем All units")
        menu_toggle = page.locator('[data-test-id="nav-mobile-menu-toggle"]')
        menu_toggle.first.wait_for(state="visible", timeout=10000)
        menu_toggle.first.click()
        page.wait_for_timeout(500)

        all_units = page.locator('[data-test-id="nav-mobile-catalog2d"]')
        all_units.first.wait_for(state="visible", timeout=10000)
        all_units.first.click()
    else:
        print("\n➡️ DESKTOP: кликаем на кнопку All units")
        all_units = page.locator(
            '[data-test-id="nav-desktop-catalog2d-standalone"]'
        )
        all_units.first.wait_for(state="visible", timeout=10000)
        all_units.first.click()

    page.wait_for_timeout(2000)
    print(f"URL каталога: {page.url}")


def navigate_to_first_apartment(page: Page):
    """Кликнуть по первой доступной квартире в каталоге и перейти на страницу apartment."""
    print("\n➡️ Ищем и кликаем на первую доступную квартиру")
    props = page.locator('[data-test-id^="property-info-primary-button-"]')
    props.first.wait_for(state="visible", timeout=10000)
    count = props.count()
    print(f"Найдено кнопок квартир: {count}")
    if count == 0:
        print("⚠️ Квартиры не найдены, дальше идти некуда")
        return

    props.first.click()
    page.wait_for_timeout(2000)
    print(f"URL квартиры: {page.url}")


def main():
    env = os.getenv("TEST_ENVIRONMENT", "dev")
    headless = os.getenv("HEADLESS", "true").lower() == "true"
    mobile_device = os.getenv("MOBILE_DEVICE")
    is_mobile = mobile_device is not None and mobile_device != "desktop"

    print("==============================================")
    print("Сбор локаторов MARK (LSR)")
    print(f"ENV={env}, HEADLESS={headless}, MOBILE_DEVICE={mobile_device}")
    print("==============================================")

    with sync_playwright() as p:
        browser_kwargs = {"headless": headless}
        browser = p.chromium.launch(**browser_kwargs)

        context_kwargs = {}
        if is_mobile:
            cfg = _get_mobile_device_config(mobile_device or "iphone_13")
            context_kwargs.update(
                viewport=cfg["viewport"],
                device_scale_factor=cfg["device_scale_factor"],
                is_mobile=cfg["is_mobile"],
                has_touch=cfg["has_touch"],
                user_agent=cfg["user_agent"],
            )

        context = browser.new_context(**context_kwargs)
        page = context.new_page()

        results: Dict[str, Dict] = {}

        # 1. MARK area
        open_mark_area_url(page)
        results["area"] = collect_page_locators(page, "area")

        # 2. area + открытое мобильное меню (если mobile)
        if is_mobile:
            print("\n➡️ MOBILE: открываем меню ещё раз для отдельного снапшота")
            menu_toggle = page.locator('[data-test-id="nav-mobile-menu-toggle"]')
            if menu_toggle.count() > 0:
                menu_toggle.first.click()
                page.wait_for_timeout(500)
                results["area_mobile_menu"] = collect_page_locators(
                    page, "area_mobile_menu"
                )
                # Закроем меню, кликнув снова
                menu_toggle.first.click()
                page.wait_for_timeout(500)

        # 3. Каталог
        navigate_to_catalog(page, is_mobile=is_mobile)
        results["catalog"] = collect_page_locators(page, "catalog")

        # 4. Страница квартиры
        navigate_to_first_apartment(page)
        results["apartment"] = collect_page_locators(page, "apartment")

        # 5. Если есть iframe с виджетом — собираем информацию о нём
        print("\n➡️ Проверяем iframe виджета апартамента")
        iframe_elements = page.locator("iframe")
        count_iframes = iframe_elements.count()
        print(f"Найдено iframe: {count_iframes}")
        widget_info = []
        for i in range(count_iframes):
            frame = page.frame_locator("iframe").nth(i)
            buttons = frame.locator("button").all()
            widget_buttons = []
            for btn in buttons:
                text = (btn.text_content() or "").strip()
                classes = btn.get_attribute("class") or ""
                widget_buttons.append(
                    {
                        "text": text[:120],
                        "classes": classes[:160],
                    }
                )
            widget_info.append(
                {
                    "index": i,
                    "buttons": widget_buttons,
                }
            )
        results["apartment_widget_iframes"] = widget_info

        browser.close()

    os.makedirs("reports", exist_ok=True)
    output_path = os.path.join("reports", "mark_all_locators.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"\n💾 Все локаторы сохранены в: {output_path}")


if __name__ == "__main__":
    main()


