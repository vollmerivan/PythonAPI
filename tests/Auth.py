from typing import Dict

import pytest
import requests

class TestUserAuth:
    exclude_params = [
        ("no_cookie"),
        ("no_token")
    ]

    def setup(selfself):
        data = {
            'email': 'rmtest@krit.pro',
            'password': 'super'
        }
        response1 = requests.post("https://riskhunter.krit.pro/api/v1/auth/SignIn", data=data)

        assert "auth_sid" in response1.cookies, "There is no auth cookie in the response"
        assert "x-csrf-token" in response1.headers, "There is no CSRF token header in the response"
        assert "user_id" in response1.json(), "There is no user id in the response"

        self.auth_sid = response1.cookies.get("auth_sid")
        self.token = response1.headers.get("x-csrf-token")
        self.user_id_from_auth_method = response1.json()["user_id"]
    def test_auth_user(self):
        response2=requests.get(
            "https://riskhunter.krit.pro/api/v1/users/me",
            headers={"x-csrf-token":self.token},
            cookies={"auth_sid":self.auth_sid}
        )

        assert "user_id" in response2.json(), "There is no user id in the response"

        user_id_from_check_method = response2.json()["user_id"]

        assert self.user_id_from_auth_method == user_id_from_check_method, "User id from auth method is not equal to user id from check method"

    @pytest.mark.parametrize('condition', exclude_params)
    def test_negativ_auth_check(self, condition):
        if condition == "no_cookie":
            response2 = requests.get(
                "https://riskhunter.krit.pro/sign-in",
                headers={"x-csrf-token":self.token}
            )
        else:
            response2=requests.get(
                "https://riskhunter.krit.pro/sign-in",
                cookies={"auth_sid":self.auth_sid}
            )

        assert "user_id" in self.response2.json(), "There is no user id in the second response"

        user_id_from_check_method = response2.json()["user_id"]

        assert user_id_from_check_method == 0, f"User is authorized with condition {condition}"
