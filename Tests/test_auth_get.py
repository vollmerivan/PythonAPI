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
        response1 = requests.post(url, json=payload)
        # Проверка кода ответа
        assert response1.status_code in [200, 401], f"Неожиданный статус ответа: {response1.status_code}"

        if response1.status_code == 200:
            print("Авторизация успешна!")
            response_data = response1.json()

            # Проверка наличия необходимых полей в ответе
            assert 'token' in response_data, "Отсутствует поле 'token' в ответе"
            print("Ответ сервера:", response_data)

        elif response1.status_code == 401:
            print("Неверный логин или пароль.")

        # Переменная response_dict создается после получения ответа от API
        response_dict = response1.json()
        # Получаем токен из ответа (предполагается, что он в формате JSON)
        token = response1.json().get('token')
        # Формируем заголовок Authorization
        Authorization = {'Authorization': f"Bearer {token}"}

        # Проверка наличия токена в ответе
        assert "token" in response_dict, "There is no field 'token' in the response"
        assert response_dict["token"] is not None, "Token should not be None"

        # отправка запроса метод гет получение списка юзеров
        response2 = requests.get("http://hunter-dev.krit.pro/api/v1/users", headers=Authorization)

        # Проверка кода ответа
        assert response2.status_code == 200, "Wrong response code"


  #провоеирим