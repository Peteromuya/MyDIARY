"""Test the users and user endpoint on all methods and covers most edge cases
"""
import unittest
import json

import sys # fix import errors
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import app
import config

app = app.create_app()
app.config.from_object('config.TestingConfig')


class UserTests(unittest.TestCase):
    """Tests functionality of the API"""


    def setUp(self):
        
        self.app = app.test_client()
        self.data = json.dumps({"username" : "balotelli", "email" : "balotelli@gmail.com",
                                "password" : "secret12345", "confirm_password" : "secret12345"})
        self.existing_user = self.app.post('/api/v1/auth/signup',
                                           data=self.data, content_type='application/json')

        
        self.data2 = json.dumps({"username" : "dan", "email" : "dan@gmail.com",
                                "password" : "secret12345", "confirm_password" : "secret12345"})
        self.existing_user = self.app.post('/api/v1/auth/signup',
                                           data=self.data2, content_type='application/json')
        

    # testing api/vi/users
    def test_get_all_users(self):
        response = self.app.get('/api/v1/users')
        self.assertEqual(response.status_code, 200)

    def test_successful_user_creation(self):
        data = json.dumps({"username" : "marcus23", "email" : "marcusrahford44@gmail.com",
                           "password" : "secret12345", "confirm_password" : "secret12345"})
        response = self.app.post('/api/v1/users', data=data, content_type='application/json')
        result = json.loads(response.data)
        self.assertEqual(result.get("username"), "marcus23")
        self.assertEqual(result.get("email"), "marcusrahford44@gmail.com")
        self.assertEqual(result.get("password"), "secret12345")
        self.assertEqual(response.status_code, 201)

    def test_user_creation_existing_email(self):
        data = json.dumps({"username" : "john", "email" : "johnmuiya24@gmail.com",
                           "password" : "secret12345", "confirm_password" : "secret12345"})
        response = self.app.post('/api/v1/users', data=data, content_type='application/json') # pylint: disable=W0612
        response2 = self.app.post('/api/v1/users', data=data, content_type='application/json')
        result = json.loads(response2.data)
        self.assertEqual(result.get("message"), "user with that email already exists")

    def test_user_creation_unmatching_passwords(self):
        data = json.dumps({"username" : "felix", "email" : "felixmutua@gmail.com",
                           "password" : "secret12345", "confirm_password" : "password12345"})
        response = self.app.post('/api/v1/users', data=data, content_type='application/json')
        result = json.loads(response.data)
        self.assertEqual(result.get("message"), "password and confirm password should be identical")

    def test_user_creation_short_passwords(self):
        data = json.dumps({"username" : "moses", "email" : "musamutua@gmail.com",
                           "password" : "123", "confirm_password" : "123"})
        response = self.app.post('/api/v1/users', data=data, content_type='application/json')
        result = json.loads(response.data)
        self.assertEqual(result.get("message"), "password should be at least 8 characters")

    def test_create_user_empty_username(self):
        data = json.dumps({"username" : "", "email" : "lennykmutua@gmail.com",
                           "password" : "secret", "confirm_password" : "secret"})
        response = self.app.post('/api/v1/users', data=data, content_type='application/json')
        result = json.loads(response.data)
        self.assertEqual(result.get("message"), {"username": "kindly provide a valid username"})

    def test_create_user_empty_email(self):
        data = json.dumps({"username" : "lenny", "email" : "",
                           "password" : "secret", "confirm_password" : "secret"})
        response = self.app.post('/api/v1/users', data=data, content_type='application/json')
        result = json.loads(response.data)
        self.assertEqual(result.get("message"), {"email": "kindly provide a valid email address"})

    def test_create_user_invalid_email(self):
        data = json.dumps({"username" : "lenny", "email" : "lennykmugmail.com",
                           "password" : "secret", "confirm_password" : "secret"})
        response = self.app.post('/api/v1/users', data=data, content_type='application/json')
        result = json.loads(response.data)
        self.assertEqual(result.get("message"), {"email": "kindly provide a valid email address"})

    def test_create_user_empty_password(self):
        data = json.dumps({"username" : "lenny", "email" : "lennymutush@gmail.com",
                           "password" : "",
                           "confirm_password" : "secret"})
        response = self.app.post('/api/v1/users', data=data, content_type='application/json')
        result = json.loads(response.data)
        self.assertEqual(result.get("message"), "password and confirm password should be identical")

    def test_user_create_empty_c_password(self):
        data = json.dumps({"username" : "lenny", "email" : "lennykmutua@gmail.com",
                           "password" : "secret", "confirm_password" : ""})
        response = self.app.post('/api/v1/users', data=data, content_type='application/json')
        result = json.loads(response.data)
        self.assertEqual(result.get("message"), "password and confirm password should be identical")

    def test_user_create_whitespace_passwords(self):
        data = json.dumps({"username" : "lenny", "email" : "lennykmutua@gmail.com",
                           "password" : "        ", "confirm_password" : "        "})
        response = self.app.post('/api/v1/users', data=data, content_type='application/json')
        result = json.loads(response.data)
        self.assertEqual(result.get("message"), "password should be at least 8 characters")


    # testing api/vi/auth/signup
    def test_successful_signup(self):
        data = json.dumps({"username" : "marcus", "email" : "marcusrashford@gmail.com",
                           "password" : "secret12345", "confirm_password" : "secret12345"})
        response = self.app.post('/api/v1/auth/signup', data=data, content_type='application/json')
        result = json.loads(response.data)
        self.assertEqual(result.get("username"), "marcus")
        self.assertEqual(result.get("email"), "marcusrashford@gmail.com")
        self.assertEqual(result.get("password"), "secret12345")
        self.assertEqual(response.status_code, 201)

    def test_signup_existing_email(self):
        data = json.dumps({"username" : "john", "email" : "johnmuiya@gmail.com",
                           "password" : "secret12345", "confirm_password" : "secret12345"})
        response = self.app.post('/api/v1/auth/signup', data=data, content_type='application/json') # pylint: disable=W0612
        response2 = self.app.post('/api/v1/auth/signup', data=data, content_type='application/json')
        result = json.loads(response2.data)
        self.assertEqual(result.get("message"), "user with that email already exists")

    def test_signup_unmatching_passwords(self):
        data = json.dumps({"username" : "felix", "email" : "felixmutua@gmail.com",
                           "password" : "secret12345", "confirm_password" : "password12345"})
        response = self.app.post('/api/v1/auth/signup', data=data, content_type='application/json')
        result = json.loads(response.data)
        self.assertEqual(result.get("message"), "password and confirm password should be identical")

    def test_signup_short_passwords(self):
        data = json.dumps({"username" : "moses", "email" : "musamutua@gmail.com",
                           "password" : "123", "confirm_password" : "123"})
        response = self.app.post('/api/v1/auth/signup', data=data, content_type='application/json')
        result = json.loads(response.data)
        self.assertEqual(result.get("message"), "password should be at least 8 characters")

    def test_signup_empty_username(self):
        data = json.dumps({"username" : "", "email" : "lennykmutua@gmail.com",
                           "password" : "secret", "confirm_password" : "secret"})
        response = self.app.post('/api/v1/auth/signup', data=data, content_type='application/json')
        result = json.loads(response.data)
        self.assertEqual(result.get("message"), {"username": "kindly provide a valid username"})

    def test_signup_empty_email(self):
        data = json.dumps({"username" : "lenny",
                           "password" : "secret", "confirm_password" : "secret"})
        response = self.app.post('/api/v1/auth/signup', data=data, content_type='application/json')
        result = json.loads(response.data)
        self.assertEqual(result.get("message"), {"email": "kindly provide a valid email address"})

    def test_signup_invalid_email(self):
        data = json.dumps({"username" : "lenny", "email" : "lennykmugmail.com",
                           "password" : "secret", "confirm_password" : "secret"})
        response = self.app.post('/api/v1/auth/signup', data=data, content_type='application/json')
        result = json.loads(response.data)
        self.assertEqual(result.get("message"), {"email": "kindly provide a valid email address"})

    def test_signup_empty_password(self):
        data = json.dumps({"username" : "lenny", "email" : "lennymutush@gmail.com",
                           "confirm_password" : "secret"})
        response = self.app.post('/api/v1/auth/signup', data=data, content_type='application/json')
        result = json.loads(response.data)
        self.assertEqual(result.get("message"), {"password": "kindly provide a valid password"})

    def test_signup_empty_confirm_password(self):
        data = json.dumps({"username" : "lenny", "email" : "lennykmutua@gmail.com",
                           "password" : "secret"})
        response = self.app.post('/api/v1/auth/signup', data=data, content_type='application/json')
        result = json.loads(response.data)
        self.assertEqual(result.get("message"), {"confirm_password": "kindly provide a valid confirmation password"})

    def test_successfully_getting_user(self):
        response = self.app.get('/api/v1/user/1')
        self.assertEqual(response.status_code, 404)

    def test_getting_non_existing_user(self):
        response = self.app.get('/api/v1/users/57')
        self.assertEqual(response.status_code, 404)

    def test_successful_user_update(self):
        data = json.dumps({ "username" : "balotelli", "email" : "mariobalotelli@gmail.com",
                           "password" : "secret12345", "confirm_password" : "secret12345"})
        response = self.app.put('/api/v1/users/1', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_updating_non_existing_user(self):
        data = json.dumps({"username" : "balotelli", "email" : "mariobalotelli@gmail.com",
                           "password" : "secret12345", "confirm_password" : "secret12345"})
        response = self.app.put('/api/v1/users/e99', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 404)

    def test_successful_user_deletion(self):
        response = self.app.delete('/api/v1/users/20')
        self.assertEqual(response.status_code, 404)

    def test_deleting_non_existing_user(self):
        response = self.app.delete('/api/v1/users/15')
        self.assertEqual(response.status_code, 404)


    # testing api/v1/auth/login
    def test_successful_login(self):
        data = json.dumps({"username" : "balotelli", "email" : "balotelli@gmail.com",
                           "password" : "secret12345", "confirm_password" : "secret12345"})
        create_user = self.app.post('/api/v1/auth/signup', data=data, content_type='application/json')
        
        login_data = json.dumps({"email" : "balotelli@gmail.com", "password" : "secret12345"})
        response = self.app.post('/api/v1/auth/login', data=login_data, content_type='application/json')
        
        result = json.loads(response.data)
        

        self.assertEqual(result.get("message"), "you have been successfully logged in")
        self.assertEqual(response.status_code, 200)


    def test_login_invalid_email(self):
        data = json.dumps({"email" : "balotelligmail.com", "password" : "secret12345"})
        response = self.app.post('/api/v1/auth/login', data=data, content_type='application/json')
        result = json.loads(response.data)
        self.assertEqual(result.get("message"), {"email": "kindly provide a valid email address"})
        self.assertEqual(response.status_code, 400)

    def test_login_wrong_email(self):
        data = json.dumps({"email" : "alotelli@gmail.com", "password" : "secret12345"})
        response = self.app.post('/api/v1/auth/login', data=data, content_type='application/json')
        result = json.loads(response.data)
        self.assertEqual(result.get("message"), "invalid email address or password")
        self.assertEqual(response.status_code, 401)

    def test_login_empty_password(self):
        data = json.dumps({"email" : "balotelli@gmail.com", "password" : ""})
        response = self.app.post('/api/v1/auth/login', data=data, content_type='application/json')
        result = json.loads(response.data)
        self.assertEqual(result.get("message"), "invalid email address or password")
        self.assertEqual(response.status_code, 401)

    def test_login_wrong_password(self):
        data = json.dumps({"email" : "balotelli@gmail.com", "password" : "mysecerto78"})
        response = self.app.post('/api/v1/auth/login', data=data, content_type='application/json')
        result = json.loads(response.data)
        self.assertEqual(result.get("message"), "invalid email address or password")
        self.assertEqual(response.status_code, 401)


if __name__ == '__main__':
    unittest.main()
