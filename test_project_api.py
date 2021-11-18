import unittest
import requests
import jwt

URL = "https://flamxby.herokuapp.com"

def login():
    endpoint = URL + "/login"
    request_body = {
        "username": "1234567848204",
        "password": "nice_password"
    }
    response = requests.post(endpoint, data=request_body, headers={"Content-Type": "application/x-www-form-urlencoded"})
    token = response.json().get("access_token")
    return token

class TestCreateReservation(unittest.TestCase):
    """Create reservation"""

    def setUp(self):
        """Initialize necessary variable"""
        self.endpoint = URL + "/reservation/"

    def test_create_reservation_but_not_login(self):
        """Create reservation but not authorize"""
        request_body = {
            "register_timestamp": "2021-10-20T17:12:39.738Z"
        }
        response = requests.post(self.endpoint, json=request_body)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.headers["Content-Type"], "application/json")
        self.assertEqual(response.json()['detail'], "Not authenticated")

    def test_create_reservation_with_fake_token(self):
        """Try to inject a fake access token and create reservation"""
        token = "fake-token"
        request_body = {
            "register_timestamp": "2021-10-20T17:12:39.738Z"
        }
        response = requests.post(self.endpoint, json=request_body, headers={"Accept": "application/json", "Authorization": f"Bearer {token}"})
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.headers["Content-Type"], "application/json")
        self.assertEqual(response.json()['detail'], "Could not validate credentials")

    def test_create_reservation_with_valid_request_body(self):
        """Create reservation with valid request body and authorize"""
        request_body = {
            "register_timestamp": "2021-10-20T17:12:39.738Z"
        }
        access_token = login()
        response = requests.post(self.endpoint, json=request_body, headers={"Accept": "application/json", "Authorization": f"Bearer {access_token}"})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.headers["Content-Type"], "application/json")
        self.assertEqual(response.json()["owner"]["citizen_id"], "1234567848204")

    def test_create_reservation_with_invalid_datetime_format(self):
        """Create reservation but register_timestamp not a valid format (ISO)"""
        request_body = {
            "register_timestamp": "Year 2021 month 10 day 21"
        }
        access_token = login()
        response = requests.post(self.endpoint, json=request_body, headers={"Accept": "application/json", "Authorization": f"Bearer {access_token}"})
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.headers["Content-Type"], "application/json")
        self.assertEqual(response.json()["detail"][0]["msg"], "invalid datetime format")

    def test_create_reservation_with_no_request_body(self):
        """Create reservation but not provide anything in the request body"""
        request_body = {}
        access_token = login()
        response = requests.post(self.endpoint, json=request_body, headers={"Accept": "application/json", "Authorization": f"Bearer {access_token}"})
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.headers["Content-Type"], "application/json")
        self.assertEqual(response.json()["detail"][0]["msg"], "field required")

class TestLogin(unittest.TestCase):
    """Login test"""

    def setUp(self):
        """Initialize necessary variable"""
        self.endpoint = URL + "/login"

    def test_login_with_valid_id(self):
        """Test with account on the database (real account)"""
        request_body = {
            "username": "1234567848204",
            "password": "nice_password"
        }
        response = requests.post(self.endpoint, data=request_body, headers={"Content-Type": "application/x-www-form-urlencoded"})
        token = response.json().get("access_token")
        token_type = response.json().get("token_type")
        decode_token = jwt.decode(token, options={"verify_signature": False})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(token_type, "bearer")
        self.assertEqual(request_body["username"], decode_token["sub"])

    def test_login_with_username_is_not_a_digit(self):
        """Username is the database must be a 13-digit (citizen id)"""
        request_body = {
            "username": "Real username",
            "password": "Real password"
        }
        response = requests.post(self.endpoint, data=request_body, headers={"Content-Type": "application/x-www-form-urlencoded"})
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.text, "Internal Server Error")

    def test_login_with_username_not_a_13_digit(self):
        """Username is the database must be a 13-digit (citizen id)"""
        request_body = {
            "username": "123",
            "password": "Real password"
        }
        response = requests.post(self.endpoint, data=request_body, headers={"Content-Type": "application/x-www-form-urlencoded"})
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.text, "Internal Server Error")

    def test_login_with_a_wrong_password(self):
        """Wrong password should not get the access token"""
        request_body = {
            "username": "1234567848204",
            "password": "not_nice_password"
        }
        response = requests.post(self.endpoint, data=request_body, headers={"Content-Type": "application/x-www-form-urlencoded"})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["detail"], "Incorrect password")

    def test_login_with_empty_request_body(self):
        """Request body required username and password field"""
        request_body = {}
        response = requests.post(self.endpoint, data=request_body, headers={"Content-Type": "application/x-www-form-urlencoded"})
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json()["detail"][0]["msg"], "field required")

if __name__ == '__main__':
    unittest.main()