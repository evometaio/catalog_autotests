import os
import time

import allure
import pytest


@allure.feature("Qube - Проект Arisha (Mobile Debug)")
@allure.story("Полная мобильная навигация с дебагом локаторов")
@pytest.mark.mobile
@pytest.mark.ui
@pytest.mark.regression
class TestArishaMobileFullNavigationDebug:
    """Мобильные тесты полной навигации по Arisha с дебагом локаторов."""

    @pytest.mark.mobile_device("iPhone 13 Pro")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_arisha_mobile_full_navigation_debug(self, mobile_map_page):
        """Полный мобильный тест навигации с дебагом локаторов."""
        
        # Дебаг функция для анализа локаторов
        def debug_locators_on_page(step_name: str):
            """Анализирует все доступные локаторы на текущей странице."""
            print(f"\n🔍 ДЕБАГ ЛОКАТОРОВ: {step_name}")
            print(f"📍 URL: {mobile_map_page.get_current_url()}")
            
            # Список локаторов для проверки
            locators_to_check = {
                "building_nav_button": mobile_map_page.project_locators.BUILDING_NAV_BUTTON,
                "floor_nav_button": mobile_map_page.project_locators.FLOOR_NAV_BUTTON,
                "apartment_nav_button": mobile_map_page.project_locators.APARTMENT_NAV_BUTTON,
                "building_1_button": mobile_map_page.project_locators.BUILDING_1_BUTTON,
                "building_2_button": mobile_map_page.project_locators.BUILDING_2_BUTTON,
                "floor_1_button": mobile_map_page.project_locators.FLOOR_1_BUTTON,
                "floor_2_button": mobile_map_page.project_locators.FLOOR_2_BUTTON,
                "floor_plan_apartments": mobile_map_page.project_locators.FLOOR_PLAN_APARTMENTS,
                "all_buttons": "button",
                "mobile_navigation": '[class*="_showOnMobiles_"]',
                "desktop_only": '[class*="_showOnDesktops_"]',
                "project_info": 'div.ant-card[class*="_projectInfo"]',
            }
            
            for locator_name, selector in locators_to_check.items():
                try:
                    elements = mobile_map_page.page.locator(selector)
                    count = elements.count()
                    visible_count = 0
                    
                    for i in range(count):
                        if elements.nth(i).is_visible():
                            visible_count += 1
                    
                    status = "✅" if visible_count > 0 else "❌"
                    print(f"{status} {locator_name}: {count} элементов, {visible_count} видимых")
                    
                    if visible_count > 0 and locator_name in ["building_nav_button", "floor_nav_button", "apartment_nav_button"]:
                        # Получаем дополнительную информацию для важных элементов
                        first_element = elements.first
                        try:
                            classes = first_element.evaluate("el => el.className")
                            text = first_element.text_content()
                            print(f"   📝 Классы: {classes}")
                            print(f"   📝 Текст: {text}")
                        except:
                            pass
                            
                except Exception as e:
                    print(f"⚠️ {locator_name}: Ошибка - {str(e)}")
            
            # Делаем скриншот для документации
            timestamp = int(time.time())
            screenshot_name = f"debug_{step_name.lower().replace(' ', '_')}_{timestamp}.png"
            screenshot_path = f"debug_screenshots/{screenshot_name}"
            os.makedirs("debug_screenshots", exist_ok=True)
            mobile_map_page.page.screenshot(path=screenshot_path, full_page=True)
            print(f"📸 Скриншот: {screenshot_path}")
            
            allure.attach(
                f"Debug info for {step_name}\nURL: {mobile_map_page.get_current_url()}", 
                name=f"Debug - {step_name}",
                attachment_type=allure.attachment_type.TEXT
            )

        with allure.step("1. Открываем мобильную карту и переходим к проекту Arisha"):
            mobile_map_page.open(route_type="map")
            debug_locators_on_page("Карта загружена")
            
            # Кликаем по проекту Arisha (используем прямой селектор)
            mobile_map_page.click(mobile_map_page.project_locators.Arisha.MAP_LOCATOR)
            time.sleep(2)  # Даем время на загрузку
            debug_locators_on_page("Проект Arisha выбран")
            
            # Кликаем на кнопку "Explore Project" (мобильная версия)
            mobile_map_page.click('[data-test-id="map-project-point-button-mobile-arisha"]')
            time.sleep(2)
            debug_locators_on_page("Explore Project нажат")

        with allure.step("2. Пытаемся найти и кликнуть на кнопку Building Navigation"):
            debug_locators_on_page("Перед выбором здания")
            
            try:
                # Пробуем найти кнопку навигации по зданиям
                building_nav = mobile_map_page.page.locator(mobile_map_page.project_locators.BUILDING_NAV_BUTTON)
                if building_nav.is_visible():
                    mobile_map_page.click(mobile_map_page.project_locators.BUILDING_NAV_BUTTON)
                    print("✅ Building nav button найден и кликнут")
                else:
                    print("❌ Building nav button не найден или не видим")
                    
                debug_locators_on_page("После клика на Building Nav")
                
            except Exception as e:
                print(f"❌ Ошибка при клике на Building Nav: {e}")
                debug_locators_on_page("Ошибка Building Nav")

        with allure.step("3. Пытаемся выбрать здание 1"):
            try:
                building_1 = mobile_map_page.page.locator(mobile_map_page.project_locators.BUILDING_1_BUTTON)
                if building_1.is_visible():
                    mobile_map_page.click(mobile_map_page.project_locators.BUILDING_1_BUTTON)
                    print("✅ Building 1 button найден и кликнут")
                    
                    # Ждем изменения URL
                    try:
                        mobile_map_page.page.wait_for_url("**/building/1", timeout=10000)
                        current_url = mobile_map_page.get_current_url()
                        print(f"✅ URL изменился на здание 1: {current_url}")
                        allure.attach(f"URL после выбора здания 1: {current_url}", name="Building 1 URL")
                    except:
                        print("⚠️ URL не изменился на building/1")
                        
                else:
                    print("❌ Building 1 button не найден или не видим")
                    
                debug_locators_on_page("После выбора здания 1")
                
            except Exception as e:
                print(f"❌ Ошибка при выборе Building 1: {e}")
                debug_locators_on_page("Ошибка Building 1")

        with allure.step("4. Пытаемся найти и кликнуть на кнопку Floor Navigation"):
            try:
                floor_nav = mobile_map_page.page.locator(mobile_map_page.project_locators.FLOOR_NAV_BUTTON)
                if floor_nav.is_visible():
                    mobile_map_page.click(mobile_map_page.project_locators.FLOOR_NAV_BUTTON)
                    print("✅ Floor nav button найден и кликнут")
                else:
                    print("❌ Floor nav button не найден или не видим")
                    
                debug_locators_on_page("После клика на Floor Nav")
                
            except Exception as e:
                print(f"❌ Ошибка при клике на Floor Nav: {e}")
                debug_locators_on_page("Ошибка Floor Nav")

        with allure.step("5. Пытаемся выбрать этаж 1"):
            try:
                floor_1 = mobile_map_page.page.locator(mobile_map_page.project_locators.FLOOR_1_BUTTON)
                if floor_1.is_visible():
                    mobile_map_page.click(mobile_map_page.project_locators.FLOOR_1_BUTTON)
                    print("✅ Floor 1 button найден и кликнут")
                    
                    # Ждем изменения URL
                    try:
                        mobile_map_page.page.wait_for_url("**/floor/1/1", timeout=10000)
                        current_url = mobile_map_page.get_current_url()
                        print(f"✅ URL изменился на этаж 1: {current_url}")
                        allure.attach(f"URL после выбора этажа 1: {current_url}", name="Floor 1 URL")
                    except:
                        print("⚠️ URL не изменился на floor/1/1")
                        
                else:
                    print("❌ Floor 1 button не найден или не видим")
                    
                debug_locators_on_page("После выбора этажа 1")
                
            except Exception as e:
                print(f"❌ Ошибка при выборе Floor 1: {e}")
                debug_locators_on_page("Ошибка Floor 1")

        with allure.step("6. Ищем апартаменты на плане этажа"):
            try:
                # Ждем загрузки плана этажа
                mobile_map_page.page.wait_for_selector(
                    mobile_map_page.project_locators.FLOOR_PLAN_APARTMENTS, timeout=10000
                )
                
                apartment_elements = mobile_map_page.page.locator(
                    mobile_map_page.project_locators.FLOOR_PLAN_APARTMENTS
                )
                apartment_count = apartment_elements.count()
                print(f"📊 Найдено апартаментов на этаже: {apartment_count}")
                allure.attach(
                    f"Найдено апартаментов на этаже: {apartment_count}", name="Apartment Count"
                )
                
                debug_locators_on_page("План этажа загружен")
                
                if apartment_count > 0:
                    with allure.step("7. Пытаемся кликнуть на первый доступный апартамент"):
                        try:
                            apartment_clicked = mobile_map_page.click_available_apartment()
                            if apartment_clicked:
                                print("✅ Апартамент успешно выбран")
                                debug_locators_on_page("Апартамент выбран")
                            else:
                                print("❌ Не удалось выбрать апартамент")
                        except Exception as e:
                            print(f"❌ Ошибка при выборе апартамента: {e}")
                else:
                    print("❌ Апартаменты на плане этажа не найдены")
                    
            except Exception as e:
                print(f"❌ Ошибка при поиске апартаментов: {e}")
                debug_locators_on_page("Ошибка поиска апартаментов")

        with allure.step("8. Финальная информация"):
            final_url = mobile_map_page.get_current_url()
            print(f"🏁 Финальный URL: {final_url}")
            allure.attach(f"Финальный URL: {final_url}", name="Final URL")
            
            debug_locators_on_page("Финальное состояние")
            
            # Проверяем, что мы на странице апартамента
            if "/apartment/" in final_url or "/unit/" in final_url:
                print("✅ Успешно дошли до страницы апартамента")
            else:
                print(f"⚠️ Не на странице апартамента. URL: {final_url}")
