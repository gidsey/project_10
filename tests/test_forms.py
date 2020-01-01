from peewee import *
import json
import unittest

from models import User, Todo
from forms import RegisterForm, LoginForm

from app import app

MODELS = [User, Todo]

db = SqliteDatabase('todo.sqlite')


class TodoTestCase(unittest.TestCase):
    def setUp(self):
        """Set up the unit tests."""
        self.app = app
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.app.testing = True
        self.client = app.test_client()

        db.bind(MODELS, bind_refs=False, bind_backrefs=False)
        db.connect()
        db.create_tables(MODELS)

        self.test_user_3 = User.create_user(
            username='tester_3',
            email='tester_3@test.com',
            password='password'
        )

    def tearDown(self):
        db.drop_tables(MODELS)
        db.close()

    def test_good_registration(self):
        data = {
            'username': 'tester_5',
            'email': 'tester_5@example.com',
            'password': 'password',
            'password2': 'password'
        }
        response = self.client.post('/register', data=data)
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_bad_registration_pw(self):
        data = {
            'username': 'tester_5',
            'email': 'tester_5@example.com',
            'password': 'password',
            'password2': 'pasSSword'
        }
        response = self.client.post('/register', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Passwords must match', response.data)

    def test_bad_registration_user_exists(self):
        data = {
            'username': 'tester_3',
            'email': 'tester_5@example.com',
            'password': 'password',
            'password2': 'pasSSword'
        }

        response = self.client.post('/register', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'User with that name already exists.', response.data)

    def test_bad_registration_email_exists(self):
        data = {
            'username': 'tester_5',
            'email': 'tester_3@test.com',
            'password': 'password',
            'password2': 'pasSSword'
        }
        response = self.client.post('/register', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'User with that email already exists.', response.data)

    def test_good_login(self):
        data = {
            'email': 'tester_3@test.com',
            'password': 'password',
        }
        response = self.client.post('/login', data=data)
        self.assertEqual(response.status_code, 302)  # Redirect to homepage

    def test_bad_login_invalid_email(self):
        data = {
            'email': 'tester_33',
            'password': 'password',
        }
        response = self.client.post('/login', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Invalid email address.', response.data)

    def test_bad_login_email_unknown(self):
        data = {
            'email': 'tester_33@test.com',
            'password': 'password',
        }
        response = self.client.post('/login', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Your email or password does not match.', response.data)

    def test_bad_login_incorrect_password(self):
        data = {
            'email': 'tester_3@test.com',
            'password': 'pa$$word',
        }
        response = self.client.post('/login', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Your email or password does not match.', response.data)
