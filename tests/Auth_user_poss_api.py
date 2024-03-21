from typing import Dict

import pytest
import requests
from lib.base_case import BaseCase

class TestUserAuth(BaseCase):
    exclude_params = [
        ("no_cookie"),
        ("no_token")
    ]
    def setup(self):
        data = {
            'email':'rmtest@krit.pro',
            'password':'super'
        }
        response1=requests.post("https://riskhunter.krit.pro/api/v1/auth/SignIn", data=data)

        self.auth_sid = self.get_cookie(response1, "auth_sid")
        self.token = self.get_header(response1, "x-csrf-token")
        self.user_id_from_auth_method = self.get_json_value(response1, "user_id")
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