from typing import Dict

import pytest
import requests

class TestUserAuth:
    def test_auth_user(self):
        data = {
            'email':'rmtest@krit.pro',
            'password':'super'
        }
        response1=requests.post("https://riskhunter.krit.pro/sign-in", data=data)

        assert "auth_sid" in response1.cookies, "There is no auth cookie in the response"
        assert "x-csrf-token" in response1.headers, "There is no CSRF token header in the response"
        assert "user_id" in response1.json(), "There is no user id in the response"

        auth_sid = response1.cookies.get("auth_sid")
        token=response1.headers.get("x-csrf-token")
        user_id_from_auth_method=response1.json()["user_id"]

        response2=requests.get(
            "https://riskhunter.krit.pro/sign-in",
            headers={"x-csrf-token":token},
            cookies={"auth_sid":auth_sid}
        )

        assert "user_id" in response2.json(), "There is no user id in the response"

        user_id_from_check_method = response2.json()["user_id"]

        assert user_id_from_auth_method == user_id_from_check_method, "User id from auth method is not equal to user id from check method"

    exclude_params = [
            ("no_cookie"),
            ("no_token")
    ]

    @pytest.mark.parametrize('condition', exclude_params)
    def test_negativ_auth_check(self, condition):
        data = {
            'email': 'rmtest@krit.pro',
            'password': 'super'
        }
        response1 = requests.post("https://riskhunter.krit.pro/sign-in", data=data)

        assert "auth_sid" in response1.cookies, "There is no auth cookie in the response"
        assert "x-csrf-token" in response1.headers, "There is no CSRF token header in the response"
        assert "user_id" in response1.json(), "There is no user id in the response"

        auth_sid = response1.cookies.get("auth_sid")
        token = response1.headers.get("x-csrf-token")

        if condition == "no_cookie":
            response2 = requests.get(
                "https://riskhunter.krit.pro/sign-in",
                headers={"x-csrf-token":token}
            )
        else:
            response2=requests.get(
                "https://riskhunter.krit.pro/sign-in",
                cookies={"auth_sid":auth_sid}
            )

        assert "user_id" in response1.json(), "There is no user id in the second response"

        user_id_from_check_method = response2.json()["user_id"]

        assert user_id_from_check_method == 0, f"User is authorized with condition {condition}"
