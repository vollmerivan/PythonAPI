import requests

# Данные для авторизации
url = 'http://hunter-dev.krit.pro/api/v1/auth/SignIn'
data = {
    'email': '123@krit.pro',
    'password': '123'
}

# Выполнение POST запроса
try:
    response = requests.post(url, json=data)

    # Проверка статуса ответа
    assert response.status_code in [200, 401], f"Неожиданный статус ответа: {response.status_code}"

    if response.status_code == 200:
        print("Авторизация успешна!")
        response_data = response.json()

        # Проверка наличия необходимых полей в ответе
        assert 'token' in response_data, "Отсутствует поле 'token' в ответе"
        print("Ответ сервера:", response_data)

    elif response.status_code == 401:
        print("Неверный логин или пароль.")

except requests.exceptions.RequestException as e:
    print(f"Произошла ошибка при выполнении запроса: {e}")
except AssertionError as assert_error:
    print(f"Ошибка проверки: {assert_error}")

    # провоеирим