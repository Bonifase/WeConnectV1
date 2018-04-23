import os
from app import app

import unittest
import tempfile
import json
from flask import jsonify

from app.models.user import User


class AppTestCase(unittest.TestCase):

    def setUp(self):
        app.testing = True
        self.app = app.test_client()
        self.data = {"username": "john",
                     "email": "email@gmail.com", "password": "&._12345"}
        self.data2 = {"username": "Bill",
                      "email": "bill@gmail.com", "password": "&._12345k"}
        self.data3 = {"username": "Bills",
                      "email": "bills@gmail.com", "password": "1234567"}
        self.data4 = {"": "james", "email": "jamess@gmail.com",
                      "password": "12345678"}
        self.data5 = {"username": "john",
                      "password": "&._12345", "newpassword": "123456789"}
        self.data6 = {"username": "john", "password": "123456789"}
        self.data7 = {"username": "", "password": "123456789"}
        self.data8 = {"username": "john",
                      "email": "uhiuhuyguygy", "newpassword": "123456789"}
        self.data9 = {"username": "john",
                      "password": "._12345", "newpassword": "123456789"}
        self.data10 = {"username": "john",
                       "password": "&._12345", "newpassword": "&._12345"}
        self.data11 = {"username": "user",
                       "email": "user@gmail.com", "password": "45"}
        self.data12 = {"username": "john",
                     "email": "email@gmail.com", "password": "._12345"}

        # Default user
        self.app.post('/api/v1/auth/register',
                      data=json.dumps(self.data), content_type='application/json')

    def tearDown(self):
        User.users.clear()

    def test_missing_username(self):
        response = self.app.post(
            '/api/v1/auth/register', data=json.dumps(self.data4), content_type='application/json')
        result = json.loads(response.data.decode())
        self.assertEqual(result["message"], "Missing key")
        self.assertEqual(response.status_code, 409)

    def test_ivalid_username(self):
        response = self.app.post(
            '/api/v1/auth/register', data=json.dumps(self.data7), content_type='application/json')
        result = json.loads(response.data.decode())
        self.assertEqual(result["error"], "Invalid username")
        self.assertEqual(response.status_code, 409)

    def test_invalid_email(self):
        response = self.app.post(
            '/api/v1/auth/register', data=json.dumps(self.data8), content_type='application/json')
        result = json.loads(response.data.decode())
        self.assertEqual(result["error"], "Invalid email")
        self.assertEqual(response.status_code, 409)

    def test_invalid_password(self):
        response = self.app.post(
            '/api/v1/auth/register', data=json.dumps(self.data11), content_type='application/json')
        result = json.loads(response.data.decode())
        print('ggggrgrgrgrg', result)
        self.assertEqual(result["error"], "Invalid password")
        self.assertEqual(response.status_code, 409)

    def test_register_user(self):
        response = self.app.post(
            '/api/v1/auth/register', data=json.dumps(self.data2), content_type='application/json')
        result = json.loads(response.data.decode())
        self.assertEqual(result["message"], "Registration Successful")
        self.assertEqual(response.status_code, 201)

    def test_duplicate_register(self):
        response2 = self.app.post(
            '/api/v1/auth/register', data=json.dumps(self.data), content_type='application/json')
        result2 = json.loads(response2.data.decode())
        self.assertEqual(result2["message"], "Email already taken")
        self.assertEqual(response2.status_code, 409)

    def test_login(self):
        response = self.app.post(
            '/api/v1/auth/login', data=json.dumps(self.data), content_type='application/json')
        result = json.loads(response.data.decode())
        self.assertEqual(result["message"], "Login Successful")
        self.assertEqual(response.status_code, 200)

    def test_wrong_password(self):
        self.app.post(
            '/api/v1/auth/register', data=json.dumps(self.data), content_type='application/json')
        response = self.app.post(
            '/api/v1/auth/login', data=json.dumps(self.data9), content_type='application/json')
        result = json.loads(response.data.decode())
        self.assertEqual(result["message"], "Wrong Password")
        self.assertEqual(response.status_code, 409)

    def test_empty_login(self):
        response = self.app.post(
            '/api/v1/auth/login', data=json.dumps(self.data7), content_type='application/json')
        result = json.loads(response.data.decode())
        self.assertTrue(result["message"], "Incomplete entry")
        self.assertEqual(response.status_code, 401)

    def test_unregistered_user(self):
        response = self.app.post(
            '/api/v1/auth/login', data=json.dumps(self.data3), content_type='application/json')
        result = json.loads(response.data.decode())
        self.assertEqual(result["message"], "Wrong username")
        self.assertEqual(response.status_code, 409)

    def test_logged_in_users(self):
        self.app.post('/api/v1/auth/register',
                      data=json.dumps(self.data), content_type='application/json')
        response = self.app.post('/api/v1/auth/reset-password',
                                 data=json.dumps(self.data5), content_type='application/json')
        result = json.loads(response.data.decode())
        self.assertEqual(result["Unauthorised"], "Please login first")
        self.assertEqual(response.status_code, 401)

    def test_reset_password(self):
        self.app.post('/api/v1/auth/register',
                      data=json.dumps(self.data), content_type='application/json')
        self.app.post('/api/v1/auth/login', data=json.dumps(self.data),
                      content_type='application/json')
        response1 = self.app.post('/api/v1/auth/reset-password',
                                  data=json.dumps(self.data5), content_type='application/json')
        result1 = json.loads(response1.data.decode())
        self.assertEqual(result1["message"], "Reset Successful")
        self.assertEqual(response1.status_code, 201)
        response2 = self.app.post(
            '/api/v1/auth/login', data=json.dumps(self.data6), content_type='application/json')
        result2 = json.loads(response2.data.decode())
        self.assertEqual(result2["message"], "Login Successful")
        self.assertEqual(response2.status_code, 200)

    def test_current_password(self):
        self.app.post('/api/v1/auth/register',
                      data=json.dumps(self.data), content_type='application/json')
        self.app.post('/api/v1/auth/login', data=json.dumps(self.data),
                      content_type='application/json')
        response1 = self.app.post('/api/v1/auth/reset-password',
                                  data=json.dumps(self.data9), content_type='application/json')
        result1 = json.loads(response1.data.decode())
        self.assertEqual(result1["message"], "Enter your Current Password")
        self.assertEqual(response1.status_code, 409)

    def test_same_password(self):
        self.app.post('/api/v1/auth/register',
                      data=json.dumps(self.data), content_type='application/json')
        self.app.post('/api/v1/auth/login', data=json.dumps(self.data),
                      content_type='application/json')
        response1 = self.app.post('/api/v1/auth/reset-password',
                                  data=json.dumps(self.data10), content_type='application/json')
        result1 = json.loads(response1.data.decode())
        self.assertEqual(result1["message"], "Use a Different New Password")
        self.assertEqual(response1.status_code, 409)

    def test_logout(self):
        response = self.app.post(
            '/api/v1/auth/login', data=json.dumps(self.data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response1 = self.app.post(
            '/api/v1/auth/logout', data=json.dumps(self.data), content_type='application/json')
        result1 = json.loads(response1.data.decode())
        self.assertEqual(result1["message"], "Logout Successful")
        self.assertEqual(response1.status_code, 200)

    def test_logout_wrong_user(self):
        self.app.post(
            '/api/v1/auth/login', data=json.dumps(self.data), content_type='application/json')
        response = self.app.post(
            '/api/v1/auth/logout', data=json.dumps(self.data12), content_type='application/json')
        result = json.loads(response.data.decode())
        self.assertEqual(result["message"], "Login First")
        self.assertEqual(response.status_code, 404)

    def test_logout_wrong_user(self):
        self.app.post(
            '/api/v1/auth/login', data=json.dumps(self.data), content_type='application/json')
        response1 = self.app.post(
            '/api/v1/auth/logout', data=json.dumps(self.data11), content_type='application/json')
        result1 = json.loads(response1.data.decode())
        self.assertEqual(result1["message"], "User not found, Login First")
        self.assertEqual(response1.status_code, 404)


if __name__ == '__main__':
    unittest.main()
