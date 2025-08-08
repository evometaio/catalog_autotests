import allure
import pytest
from utils.api_client import APIClient


@allure.feature("API Testing")
@allure.story("Пример API тестов")
class TestAPIExample:
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Инициализация API клиента."""
        self.api_client = APIClient()
    
    @pytest.mark.smoke
    @pytest.mark.api
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.step("Тест GET запроса")
    def test_get_request(self):
        """Тест GET запроса к публичному API."""
        # Используем JSONPlaceholder как пример публичного API
        self.api_client.base_url = "https://jsonplaceholder.typicode.com"
        
        response = self.api_client.get("posts/1")
        
        # Проверяем статус код
        self.api_client.expect_status_code(response, 200)
        
        # Проверяем структуру ответа
        data = response.json()
        assert "id" in data
        assert "title" in data
        assert "body" in data
        assert "userId" in data
        
        # Проверяем конкретные значения
        assert data["id"] == 1
        assert data["userId"] == 1
    
    @pytest.mark.smoke
    @pytest.mark.api
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.step("Тест POST запроса")
    def test_post_request(self):
        """Тест POST запроса к публичному API."""
        self.api_client.base_url = "https://jsonplaceholder.typicode.com"
        
        post_data = {
            "title": "Test Post",
            "body": "This is a test post",
            "userId": 1
        }
        
        response = self.api_client.post("posts", json=post_data)
        
        # Проверяем статус код (201 для создания)
        self.api_client.expect_status_code(response, 201)
        
        # Проверяем ответ
        data = response.json()
        assert data["title"] == post_data["title"]
        assert data["body"] == post_data["body"]
        assert data["userId"] == post_data["userId"]
        assert "id" in data  # Должен быть создан новый ID
    
    @pytest.mark.regression
    @pytest.mark.api
    @allure.severity(allure.severity_level.NORMAL)
    @allure.step("Тест PUT запроса")
    def test_put_request(self):
        """Тест PUT запроса к публичному API."""
        self.api_client.base_url = "https://jsonplaceholder.typicode.com"
        
        update_data = {
            "id": 1,
            "title": "Updated Title",
            "body": "Updated body content",
            "userId": 1
        }
        
        response = self.api_client.put("posts/1", json=update_data)
        
        # Проверяем статус код
        self.api_client.expect_status_code(response, 200)
        
        # Проверяем обновленные данные
        data = response.json()
        assert data["title"] == update_data["title"]
        assert data["body"] == update_data["body"]
    
    @pytest.mark.regression
    @pytest.mark.api
    @allure.severity(allure.severity_level.NORMAL)
    @allure.step("Тест DELETE запроса")
    def test_delete_request(self):
        """Тест DELETE запроса к публичному API."""
        self.api_client.base_url = "https://jsonplaceholder.typicode.com"
        
        response = self.api_client.delete("posts/1")
        
        # Проверяем статус код
        self.api_client.expect_status_code(response, 200)
    
    @pytest.mark.regression
    @pytest.mark.api
    @allure.severity(allure.severity_level.MINOR)
    @allure.step("Тест обработки ошибок")
    def test_error_handling(self):
        """Тест обработки ошибок API."""
        self.api_client.base_url = "https://jsonplaceholder.typicode.com"
        
        # Запрос к несуществующему ресурсу
        response = self.api_client.get("posts/999999")
        
        # Проверяем статус код 404
        self.api_client.expect_status_code(response, 404)
    
    @pytest.mark.regression
    @pytest.mark.api
    @allure.severity(allure.severity_level.MINOR)
    @allure.step("Тест с параметрами запроса")
    def test_query_parameters(self):
        """Тест GET запроса с параметрами."""
        self.api_client.base_url = "https://jsonplaceholder.typicode.com"
        
        params = {
            "userId": 1,
            "_limit": 3
        }
        
        response = self.api_client.get("posts", params=params)
        
        # Проверяем статус код
        self.api_client.expect_status_code(response, 200)
        
        # Проверяем количество постов
        data = response.json()
        assert len(data) <= 3  # Ограничение по _limit
        
        # Проверяем, что все посты принадлежат пользователю с userId=1
        for post in data:
            assert post["userId"] == 1
