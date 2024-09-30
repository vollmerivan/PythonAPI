import requests


#данные для авторизации
payload = {"email": "1233@krit.pro", "password": "123"}

#отправка запроса пост авторизации
response1 = requests.post("http://hunter-dev.krit.pro/api/v1/auth/SignIn", json=payload)

# Получаем токен из ответа (предполагается, что он в формате JSON)
token = response1.json().get('token')
# Формируем заголовок Authorization
Authorization = {'Authorization': f"Bearer {token}"}

#отправка запроса метод гет получение списка юзеров
response2 = requests.get("http://hunter-dev.krit.pro/api/v1/users", headers=Authorization)


print(response1.status_code)
print(response1.text)
print(response2.status_code)
print(response2.text)
