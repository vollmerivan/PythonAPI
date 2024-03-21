import requests

payload = {"login": "secret_login", "password": "secret_pass2"}
response1 = requests.post("https://riskhunter.krit.pro/sign-in", data=payload)

cookie_value = response1.cookies.get('auth_cookie')

cookies = {}
if cookie_value is not None:
    cookies.update({'auth_cookie': cookie_value})

response2 = requests.post("https://riskhunter.krit.pro/sign-in", cookies=cookies)

print(response2.text)
