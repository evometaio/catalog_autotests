"""Отладочный скрипт для 360 Area Tour проекта MARK.

Скрипт повторяет шаги теста `test_mark_360_area_tour`:
- открывает страницу MARK;
- кликает на кнопку 360 Area Tour;
- выбирает тип панорамы;
- для rotation проверяет модальное окно и контент;
- для остальных проверяет URL и наличие iframe.

Запуск:
    TEST_ENVIRONMENT=dev DEV_LSR_MARK_BASE_URL=<url> HEADLESS=false \\
    python debug_mark_360_area_tour.py --panorama rotation

Параметры:
    --panorama / -p: rotation, yard, lobby-k1, lobby-k2, lobby-k3 или all
"""

import argparse
import os
import time

from playwright.sync_api import sync_playwright

from conftest import _get_urls_by_environment, MOBILE_DEVICES
from pages.projects.lsr.mark_page import MarkPage


PANORAMA_TYPES = ["rotation", "yard", "lobby-k1", "lobby-k2", "lobby-k3"]


def _launch_browser(playwright):
    """Запустить браузер для отладки (desktop или mobile в зависимости от MOBILE_DEVICE)."""
    browser_name = os.getenv("DEBUG_BROWSER", "chromium")
    headless = os.getenv("HEADLESS", "false").lower() == "true"
    device = os.getenv("MOBILE_DEVICE", "desktop")

    if not hasattr(playwright, browser_name):
        raise ValueError(
            f"Неизвестный браузер '{browser_name}'. "
            f"Доступные варианты: chromium, firefox, webkit"
        )

    browser_type = getattr(playwright, browser_name)
    browser = browser_type.launch(
        headless=headless,
        args=[
            "--no-sandbox",
            "--disable-dev-shm-usage",
        ],
    )

    if device != "desktop":
        # Мобильная конфигурация как в conftest.py
        config = MOBILE_DEVICES.get(device, MOBILE_DEVICES["iphone_13"])
        print(
            f"Используем мобильное устройство: {device} "
            f"{config['viewport']['width']}x{config['viewport']['height']}"
        )
        context = browser.new_context(
            viewport=config["viewport"],
            device_scale_factor=config["device_scale_factor"],
            is_mobile=config["is_mobile"],
            has_touch=config["has_touch"],
            user_agent=config["user_agent"],
            ignore_https_errors=True,
            accept_downloads=True,
        )
    else:
        # Десктопная конфигурация
        print("Используем десктопную конфигурацию 1920x1080")
        context = browser.new_context(
            viewport={"width": 1920, "height": 1080},
            ignore_https_errors=True,
            accept_downloads=True,
        )

    return browser, context


def _debug_360_button_state(page, project_locators):
    """Вывести отладочную информацию по кнопке 360 Area Tour."""
    selector = project_locators.AREA_TOUR_360_BUTTON
    locator = page.locator(selector)
    count = locator.count()
    print(f"[DEBUG] Кнопка 360 Area Tour: селектор='{selector}', элементов={count}")

    # Если элементов нет, пробуем мобильный XPath-вариант (как в MobilePage)
    if count == 0:
        mobile_xpath = (
            'xpath=(//button[@data-test-id="nav-rotation-view-controls-button"])'
        )
        locator = page.locator(mobile_xpath)
        count = locator.count()
        print(
            f"[DEBUG] Через XPath (mobile) селектор='{mobile_xpath}', элементов={count}"
        )

    for idx in range(count):
        button = locator.nth(idx)
        try:
            visible = button.is_visible()
        except Exception:
            visible = False
        try:
            box = button.bounding_box()
        except Exception:
            box = None

        print(f"  - index={idx}, visible={visible}, bounding_box={box}")


def _scan_potential_360_buttons(page):
    """Поиск ВСЕХ потенциальных элементов 360/панорам по любым признакам во всех фреймах."""
    frames = page.frames
    print(f"[DEBUG] Количество фреймов на странице: {len(frames)}")
    
    keywords = ["360", "панора", "panorama", "tour", "панорамы", "rotation", "view", "controls"]
    
    for frame_idx, frame in enumerate(frames):
        print(f"[DEBUG] Фрейм #{frame_idx}: url={frame.url!r}, name={frame.name!r}")
        
        # 1. Ищем все элементы с data-test-id, содержащие ключевые слова
        print("  [DEBUG] Поиск элементов с data-test-id...")
        all_elements_with_test_id = frame.locator('[data-test-id*="rotation"], [data-test-id*="tour"], [data-test-id*="360"], [data-test-id*="panorama"], [data-test-id*="view"], [data-test-id*="controls"]')
        total_test_id = all_elements_with_test_id.count()
        print(f"    Найдено элементов с data-test-id: {total_test_id}")
        
        for idx in range(min(total_test_id, 30)):
            elem = all_elements_with_test_id.nth(idx)
            try:
                tag_name = elem.evaluate("el => el.tagName")
            except Exception:
                tag_name = "unknown"
            try:
                text = (elem.inner_text() or "").strip()[:100]
            except Exception:
                text = ""
            try:
                data_test_id = elem.get_attribute("data-test-id")
            except Exception:
                data_test_id = None
            try:
                visible = elem.is_visible()
            except Exception:
                visible = False
            try:
                class_name = elem.get_attribute("class") or ""
            except Exception:
                class_name = ""
                
            print(
                f"    [DATA-TEST-ID] idx={idx}, tag={tag_name}, visible={visible}, "
                f"data-test-id={data_test_id!r}, class={class_name[:50]!r}, text={text!r}"
            )
        
        # 2. Ищем все элементы по тексту (любые теги)
        print("  [DEBUG] Поиск элементов по тексту (360/панорама/tour/rotation)...")
        candidates_by_text = []
        
        # Ищем через XPath по тексту
        for keyword in keywords:
            try:
                xpath_selector = f'//*[contains(translate(text(), "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"), "{keyword}")]'
                elements = frame.locator(f'xpath={xpath_selector}')
                count = elements.count()
                if count > 0:
                    print(f"    Найдено элементов с текстом '{keyword}': {count}")
                    for idx in range(min(count, 10)):
                        elem = elements.nth(idx)
                        try:
                            tag_name = elem.evaluate("el => el.tagName")
                            text = (elem.inner_text() or "").strip()[:100]
                            visible = elem.is_visible()
                            data_test_id = elem.get_attribute("data-test-id")
                            class_name = elem.get_attribute("class") or ""
                            candidates_by_text.append((tag_name, text, visible, data_test_id, class_name))
                        except Exception:
                            pass
            except Exception as e:
                pass
        
        # Выводим уникальных кандидатов по тексту
        seen = set()
        for tag, text, visible, data_test_id, class_name in candidates_by_text:
            key = (tag, text[:50], data_test_id)
            if key not in seen:
                seen.add(key)
                print(
                    f"    [BY-TEXT] tag={tag}, visible={visible}, "
                    f"data-test-id={data_test_id!r}, class={class_name[:50]!r}, text={text!r}"
                )
        
        # 3. Ищем все элементы по классам CSS, содержащим ключевые слова
        print("  [DEBUG] Поиск элементов по классам CSS...")
        for keyword in ["rotation", "tour", "360", "panorama", "view", "controls", "button"]:
            try:
                elements = frame.locator(f'[class*="{keyword}"]')
                count = elements.count()
                if count > 0:
                    print(f"    Найдено элементов с классом '{keyword}': {count}")
                    for idx in range(min(count, 10)):
                        elem = elements.nth(idx)
                        try:
                            tag_name = elem.evaluate("el => el.tagName")
                            text = (elem.inner_text() or "").strip()[:100]
                            visible = elem.is_visible()
                            data_test_id = elem.get_attribute("data-test-id")
                            class_name = elem.get_attribute("class") or ""
                            if any(k in class_name.lower() for k in keywords):
                                print(
                                    f"    [BY-CLASS] tag={tag_name}, visible={visible}, "
                                    f"data-test-id={data_test_id!r}, class={class_name[:80]!r}, text={text!r}"
                                )
                        except Exception:
                            pass
            except Exception:
                pass
        
        # 4. Ищем все кликабельные элементы (button, a, div/span с onclick, элементы с cursor:pointer)
        print("  [DEBUG] Поиск всех кликабельных элементов...")
        clickable = frame.locator('button, a, [role="button"], [onclick], [style*="cursor: pointer"], [style*="cursor:pointer"]')
        total_clickable = clickable.count()
        print(f"    Всего кликабельных элементов: {total_clickable}")
        
        for idx in range(min(total_clickable, 30)):
            elem = clickable.nth(idx)
            try:
                tag_name = elem.evaluate("el => el.tagName")
                text = (elem.inner_text() or "").strip()[:100]
                visible = elem.is_visible()
                data_test_id = elem.get_attribute("data-test-id")
                class_name = elem.get_attribute("class") or ""
                onclick = elem.get_attribute("onclick")
                
                # Проверяем, содержит ли элемент что-то связанное с 360/панорамами
                text_lower = text.lower()
                class_lower = class_name.lower()
                is_candidate = (
                    any(k in text_lower for k in keywords) or
                    any(k in class_lower for k in keywords) or
                    (data_test_id and any(k in data_test_id.lower() for k in keywords))
                )
                
                if is_candidate:
                    print(
                        f"    [CLICKABLE-CANDIDATE] idx={idx}, tag={tag_name}, visible={visible}, "
                        f"data-test-id={data_test_id!r}, class={class_name[:50]!r}, "
                        f"text={text!r}, onclick={bool(onclick)}"
                    )
            except Exception:
                pass


def _find_menu_items_after_360_click(page, project_locators):
    """Найти и вывести все пункты меню после клика на кнопку 360."""
    print("\n[DEBUG] === Поиск пунктов меню 360 Area Tour ===")
    
    # Ждём немного, чтобы меню успело открыться
    import time
    time.sleep(2)
    
    # Ищем все возможные элементы меню
    menu_selectors = [
        # По data-test-id
        '[data-test-id*="rotation"]',
        '[data-test-id*="tour"]',
        '[data-test-id*="lobby"]',
        '[data-test-id*="yard"]',
        # По тексту
        '//*[contains(text(), "Зиларт")]',
        '//*[contains(text(), "Дворовая")]',
        '//*[contains(text(), "Лобби")]',
        '//*[contains(text(), "корпус")]',
        '//*[contains(text(), "территория")]',
        # Общие селекторы для меню
        '.ant-dropdown-menu-item',
        '.ant-menu-item',
        '[role="menuitem"]',
        'li[class*="menu"]',
        'div[class*="menu"]',
    ]
    
    found_items = []
    
    for selector in menu_selectors:
        try:
            if selector.startswith('//'):
                elements = page.locator(f'xpath={selector}')
            else:
                elements = page.locator(selector)
            
            count = elements.count()
            if count > 0:
                print(f"\n[DEBUG] Найдено элементов по селектору '{selector}': {count}")
                for idx in range(min(count, 10)):
                    elem = elements.nth(idx)
                    try:
                        text = (elem.inner_text() or "").strip()
                        data_test_id = elem.get_attribute("data-test-id")
                        class_name = elem.get_attribute("class") or ""
                        visible = elem.is_visible()
                        tag_name = elem.evaluate("el => el.tagName")
                        
                        # Проверяем, содержит ли элемент текст, связанный с панорамами
                        text_lower = text.lower()
                        if any(k in text_lower for k in ["зиларт", "дворовая", "лобби", "корпус", "территория", "rotation", "yard", "lobby"]) or data_test_id:
                            item_info = {
                                "index": idx,
                                "tag": tag_name,
                                "text": text,
                                "data-test-id": data_test_id,
                                "class": class_name[:100],
                                "visible": visible,
                                "selector": selector
                            }
                            found_items.append(item_info)
                            print(
                                f"  [MENU ITEM] idx={idx}, tag={tag_name}, visible={visible}, "
                                f"text={text!r}, data-test-id={data_test_id!r}, class={class_name[:50]!r}"
                            )
                    except Exception as e:
                        pass
        except Exception as e:
            pass
    
    # Также ищем через известные локаторы из проекта
    if hasattr(project_locators, "AREA_TOUR_360_MENU_ITEMS"):
        print(f"\n[DEBUG] Поиск через AREA_TOUR_360_MENU_ITEMS: {project_locators.AREA_TOUR_360_MENU_ITEMS}")
        menu_items = page.locator(project_locators.AREA_TOUR_360_MENU_ITEMS)
        count = menu_items.count()
        print(f"[DEBUG] Найдено через AREA_TOUR_360_MENU_ITEMS: {count}")
        for idx in range(count):
            item = menu_items.nth(idx)
            try:
                text = (item.inner_text() or "").strip()
                data_test_id = item.get_attribute("data-test-id")
                visible = item.is_visible()
                print(f"  [MENU ITEM] idx={idx}, visible={visible}, text={text!r}, data-test-id={data_test_id!r}")
            except Exception:
                pass
    
    # Ищем конкретные пункты меню и выводим их полные локаторы
    menu_texts = ["Зиларт марк", "Дворовая территория", "Лобби корпус 1", "Лобби корпус 2", "Лобби корпус 3"]
    for menu_text in menu_texts:
        try:
            xpath = f'//*[contains(text(), "{menu_text}")]'
            elements = page.locator(f'xpath={xpath}')
            count = elements.count()
            if count > 0:
                print(f"\n[DEBUG] Найдено элементов с текстом '{menu_text}': {count}")
                for idx in range(count):
                    elem = elements.nth(idx)
                    try:
                        full_text = (elem.inner_text() or "").strip()
                        data_test_id = elem.get_attribute("data-test-id")
                        class_name = elem.get_attribute("class") or ""
                        visible = elem.is_visible()
                        tag_name = elem.evaluate("el => el.tagName")
                        
                        # Получаем родительский элемент
                        parent = elem.locator("xpath=..")
                        parent_tag = parent.evaluate("el => el.tagName") if parent.count() > 0 else "N/A"
                        parent_class = parent.get_attribute("class") or "" if parent.count() > 0 else "N/A"
                        parent_data_test_id = parent.get_attribute("data-test-id") if parent.count() > 0 else None
                        
                        # Формируем XPath локатор для этого элемента
                        xpath_locator = f'xpath=(//*[contains(text(), "{menu_text}")])[{idx+1}]'
                        
                        print(
                            f"  [FOUND] idx={idx}, tag={tag_name}, visible={visible}, "
                            f"text={full_text!r}, data-test-id={data_test_id!r}, class={class_name[:50]!r}"
                        )
                        print(
                            f"    Parent: tag={parent_tag}, class={parent_class[:50]!r}, "
                            f"data-test-id={parent_data_test_id!r}"
                        )
                        print(f"    XPath локатор: {xpath_locator}")
                    except Exception as e:
                        print(f"    Ошибка при обработке элемента: {e}")
        except Exception:
            pass
    
    print("\n[DEBUG] === Конец поиска пунктов меню ===\n")


def run_mark_360_scenario(panorama_type: str):
    """Выполнить сценарий 360 Area Tour для указанного типа панорамы."""
    env = os.getenv("TEST_ENVIRONMENT", "dev")
    if env != "dev":
        print(
            f"⚠️  TEST_ENVIRONMENT={env!r}. "
            "Оригинальный тест запускается только на dev окружении."
        )

    urls = _get_urls_by_environment()
    base_url = urls["lsr_mark"]

    print(f"\n=== Запуск сценария MARK 360 Area Tour | panorama_type={panorama_type} ===")
    print(f"Базовый URL: {base_url}")

    with sync_playwright() as p:
        browser, context = _launch_browser(p)
        page = context.new_page()

        try:
            mark_page = MarkPage(page, base_url)

            print("Шаг 1: Открываем главную страницу MARK")
            mark_page.open()
            print(f"Текущий URL: {mark_page.get_current_url()}")

            print("Шаг 2: Кликаем на кнопку 360 Area Tour (Панорамы)")

            device = os.getenv("MOBILE_DEVICE", "desktop")
            if device != "desktop":
                # Мобильный сценарий: используем XPath локатор
                button = mark_page.page.locator('xpath=(//button[@data-test-id="nav-rotation-view-controls-button"])[2]')
                print("[DEBUG] Ищем мобильную кнопку 360 через XPath: (//button[@data-test-id=\"nav-rotation-view-controls-button\"])[2]")
                print("[DEBUG] Ждём появления кнопки и кликаем...")
                button.wait_for(state="visible", timeout=10000)
                button.click()
                print("[DEBUG] ✅ Клик выполнен, ищем пункты меню...")
                
                # Ищем и выводим все пункты меню
                _find_menu_items_after_360_click(mark_page.page, mark_page.project_locators)
                
                # Ждём появления меню (любой пункт меню)
                menu_items = mark_page.page.locator(
                    mark_page.project_locators.AREA_TOUR_360_MENU_ITEMS
                )
                try:
                    menu_items.first.wait_for(state="visible", timeout=5000)
                    print("[DEBUG] ✅ Меню появилось")
                except Exception as e:
                    print(f"[DEBUG] ⚠️  Меню не появилось или уже было открыто: {e}")
                
                time.sleep(1)
            else:
                # Десктопный сценарий: используем компонент
                mark_page.area_tour_360.click_360_button()
                # Ищем и выводим все пункты меню
                _find_menu_items_after_360_click(mark_page.page, mark_page.project_locators)

            print(f"Шаг 3: Кликаем на пункт меню: {panorama_type}")
            mark_page.area_tour_360.click_360_menu_item(panorama_type)

            if panorama_type == "rotation":
                print("Шаг 4: Проверяем отображение модального окна 360 Area Tour")
                mark_page.area_tour_360.verify_modal_displayed()

                print("Шаг 5: Проверяем наличие контента в модальном окне")
                mark_page.area_tour_360.verify_content()

                # Даём время посмотреть на модалку
                wait_seconds = int(os.getenv("DEBUG_WAIT_SECONDS", "3"))
                print(
                    f"Ожидаем {wait_seconds} секунд перед закрытием модального окна..."
                )
                time.sleep(wait_seconds)

                print("Шаг 6: Закрываем модальное окно 360 Area Tour")
                mark_page.area_tour_360.close_modal()
            else:
                print(
                    "Шаг 4: Проверяем, что URL изменился "
                    "(добавился hash с типом панорамы)"
                )
                current_url = mark_page.get_current_url()
                print(f"Текущий URL после выбора панорамы: {current_url}")

                if f"#tour3d={panorama_type}" in current_url or (
                    f"tour3d={panorama_type}" in current_url
                ):
                    print("✅ URL содержит информацию о выбранной панораме")
                else:
                    print(
                        "❌ URL не содержит ожидаемую информацию о выбранной панораме"
                    )

                print("Шаг 5: Проверяем наличие контента 360 тура (iframe)")
                iframe = mark_page.page.locator("iframe")
                try:
                    iframe.first.wait_for(state="attached", timeout=10000)
                    count = iframe.count()
                    print(f"Найдено iframe на странице: {count}")
                    if count == 0:
                        print("❌ Контент 360 тура (iframe) не найден на странице")
                    else:
                        print("✅ Найден iframe с контентом 360 тура")
                except Exception as e:
                    print(f"❌ Ошибка при ожидании iframe: {e}")

                # Небольшая пауза, чтобы можно было увидеть результат
                wait_seconds = int(os.getenv("DEBUG_WAIT_SECONDS", "3"))
                print(f"Ожидаем {wait_seconds} секунд перед завершением сценария...")
                time.sleep(wait_seconds)

        finally:
            # В режиме отладки оставляем браузер открытым дольше
            if os.getenv("HEADLESS", "false").lower() == "false":
                final_wait = int(os.getenv("DEBUG_WAIT_SECONDS", "10"))
                print(f"\n⏸️  Браузер останется открытым ещё {final_wait} секунд для отладки...")
                time.sleep(final_wait)
            
            context.close()
            browser.close()


def main():
    parser = argparse.ArgumentParser(
        description="Отладочный скрипт для 360 Area Tour проекта MARK"
    )
    parser.add_argument(
        "-p",
        "--panorama",
        choices=PANORAMA_TYPES + ["all"],
        default="all",
        help=(
            "Тип панорамы: rotation, yard, lobby-k1, lobby-k2, lobby-k3 или all "
            "(по умолчанию all)"
        ),
    )

    args = parser.parse_args()

    if args.panorama == "all":
        for pt in PANORAMA_TYPES:
            run_mark_360_scenario(pt)
    else:
        run_mark_360_scenario(args.panorama)


if __name__ == "__main__":
    main()


