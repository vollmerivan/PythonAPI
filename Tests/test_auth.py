import pytest
import requests

class TestFirstAPI:
    emails = [
        ("123@krit.pro"),
        ("1223@krit.pro"),
    ]

    @pytest.mark.parametrize('email', emails)
    def test_auth(self, email):
        url = "http://hunter-dev.krit.pro/api/v1/auth/SignIn"
        payload = {"email": email, "password": "123"}

        # Отправка POST-запроса
        response = requests.post(url, json=payload)
        # Проверка кода ответа
        assert response.status_code == 200, "Wrong response code"

        # Переменная response_dict создается после получения ответа от API
        response_dict = response.json()

        # Проверка наличия токена в ответе
        assert "token" in response_dict, "There is no field 'token' in the response"
        assert response_dict["token"] is not None, "Token should not be None"



        #провоеирим

