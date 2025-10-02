import allure
import pytest


@allure.feature("Qube - Проект Cubix")
@allure.story("Клиентский роут - Форма Register Interest")
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.ui
def test_cubix_request_viewing_form_with_mock(client_page, fake):
    """Тест формы Register Interest проекта Cubix."""

    with allure.step("Открываем клиентскую страницу проекта Cubix"):
        client_page.open(route_type="client")
        
        current_url = client_page.get_current_url()
        assert "client" in current_url, "Не открылась клиентская страница"

    with allure.step("Кликаем на проект Cubix"):
        client_page.click_project_on_map("cubix")

    with allure.step("Проверяем, что мы на странице проекта Cubix"):
        current_url = client_page.get_current_url()
        assert "/cubix" in current_url, f"Не на странице проекта Cubix. URL: {current_url}"
