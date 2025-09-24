import os

import allure
import pytest


@allure.feature("Wellcube - Проект Tranquil")
@allure.story("Загрузка PDF - Fraction Ownership Offer")
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.ui
@pytest.mark.skipif(
    os.getenv("TEST_ENVIRONMENT", "dev") == "prod",
    reason="тест временно отключен на PROD",
)
def test_tranquil_download_ownership_offer(wellcube_page, agent_page):
    """Тест скачивания PDF на проектк Tranquil."""

    with allure.step("Открываем карту Wellcube"):
        wellcube_page.open(route_type="map")

    with allure.step("Кликаем на проект Tranquil"):
        wellcube_page.click_project_on_map("tranquil")

    with allure.step("Кликаем на кнопку Fraction Ownership Offer"):
        wellcube_page.click_on_fraction_ownership_offer_button()
        agent_page.click_on_download_pdf_button()

    with allure.step("Проверяем что открылась новая вкладка с PDF"):
        wellcube_page.page.wait_for_timeout(2000)
        tabs = wellcube_page.page.context.pages
        assert len(tabs) == 2, "Новая вкладка не открылась"

        new_tab = tabs[1]
        new_tab.wait_for_load_state()

        # Проверяем URL PDF
        pdf_url = new_tab.url
        expected_pattern = "evometa-backend-dev.fra1.cdn.digitaloceanspaces.com/agent-pdf/custom/tranquil/release_1/1102A.pdf"
        assert expected_pattern in pdf_url, f"Неожиданный URL PDF: {pdf_url}"

        allure.attach(
            pdf_url, name="PDF URL", attachment_type=allure.attachment_type.TEXT
        )
