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
        self.user_data = {
            "username": 'user_3',
            "email": 'user_3@example.com',
            "password": 'password',
            "verify_password": 'password'
        }

        # Bind model classes to test db. Since we have a complete list of
        # all models, we do not need to recursively bind dependencies.
        db.bind(MODELS, bind_refs=False, bind_backrefs=False)
        db.connect()
        db.create_tables(MODELS)

        self.test_user_3 = User.create_user(
            username='tester_3',
            email='tester_3@test.com',
            password='password'
        )

        self.test_user_4 = User.create_user(
            username='tester_4',
            email='tester_4test.com',
            password='password'
        )

    def format_token(self, user):
        """Return the user token in a header-friendly format."""
        self.token = user.generate_auth_token()
        return "token " + self.token.decode('ascii')

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

        response = self.client.post(
            '/register',
            data=data)
        self.assertEqual(response.status_code, 302)


    def test_bad_registration_pw(self):
        data = {
            'username': 'tester_5',
            'email': 'tester_5@example.com',
            'password': 'password',
            'password2': 'pasSSword'
        }

        response = self.client.post(
            '/register',
            data=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Passwords must match', response.data)


    def test_bad_registration_user_exists(self):
        data = {
            'username': 'tester_3',
            'email': 'tester_5@example.com',
            'password': 'password',
            'password2': 'pasSSword'
        }

        response = self.client.post(
            '/register',
            data=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'User with that name already exists.', response.data)

    def test_bad_registration_email_exists(self):
        data = {
            'username': 'tester_5',
            'email': 'tester_3@test.com',
            'password': 'password',
            'password2': 'pasSSword'
        }

        response = self.client.post(
            '/register',
            data=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'User with that email already exists.', response.data)