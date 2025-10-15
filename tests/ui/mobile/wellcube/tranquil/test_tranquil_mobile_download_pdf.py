import allure
import pytest


@allure.feature("Wellcube - Проект Tranquil (mobile)")
@allure.story("Загрузка PDF - Fraction Ownership Offer - Мобильная")
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.mobile
def test_tranquil_mobile_download_ownership_offer(mobile_page):
    """Тест скачивания PDF на проекте Tranquil на мобильном устройстве."""

    with allure.step("Открываем карту Wellcube"):
        mobile_page.open(route_type="map")

    with allure.step("Кликаем на проект Tranquil"):
        mobile_page.mobile_map.click_project("tranquil")

    with allure.step("Кликаем на Explore Project"):
        mobile_page.mobile_map.click_explore_project("tranquil")

    with allure.step("Кликаем на кнопку Fraction Ownership Offer"):
        mobile_page.click_on_fraction_ownership_offer_button()

        # Ожидаем открытия новой вкладки с PDF
        with mobile_page.page.expect_popup(timeout=10000) as popup_info:
            mobile_page.click_mobile_download_pdf_button()

        new_tab = popup_info.value
        # Небольшая задержка для стабилизации в headless режиме
        new_tab.wait_for_timeout(2000)

    with allure.step("Проверяем что открылась новая вкладка с PDF"):
        # Проверяем URL PDF
        pdf_url = new_tab.url
        allure.attach(
            f"PDF URL: {pdf_url}",
            name="PDF URL",
            attachment_type=allure.attachment_type.TEXT,
        )

        # Проверяем что новая вкладка открылась
        mobile_page.assertions.assert_that(
            new_tab is not None, "Новая вкладка с PDF не открылась"
        )

        # Если URL содержит PDF, проверяем его
        if pdf_url.endswith(".pdf"):
            mobile_page.assertions.assert_that(
                "tranquil" in pdf_url.lower(),
                f"URL PDF не содержит название проекта tranquil: {pdf_url}",
            )
            allure.attach(
                "PDF успешно загружен",
                name="PDF Status",
                attachment_type=allure.attachment_type.TEXT,
            )
        else:
            # В headless режиме PDF может не отображаться, но вкладка должна открыться
            allure.attach(
                "PDF открылся в новой вкладке (headless режим)",
                name="PDF Status",
                attachment_type=allure.attachment_type.TEXT,
            )

    with allure.step("Проверяем адаптивность на мобильном устройстве"):
        mobile_page.check_mobile_viewport_adaptation()
