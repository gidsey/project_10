from peewee import *
import json

from functools import wraps
from unittest import TestCase
from models import User, Todo
from app import app

MODELS = (User, Todo, )

test_db = SqliteDatabase(':memory:')


# Bind the given models to the db for the duration of wrapped block.
def use_test_database(fn):
    @wraps(fn)
    def inner(self):
        with test_db.bind_ctx(MODELS):
            test_db.create_tables(MODELS)
            try:
                fn(self)
            finally:
                test_db.drop_tables(MODELS)
    return inner


class TestUsers(TestCase):
    @staticmethod
    def create_users(count=2):
        for i in range(count):
            User.create_user(
                username='user_{}'.format(i),
                email='test_{}@example.com'.format(i),
                password='password',
            )

    @use_test_database
    def test_create_user(self):
        self.create_users()
        self.assertEqual(User.select().count(), 2)
        self.assertNotEqual(
            User.select().get().password,
            'password'
        )

    @use_test_database
    def test_create_duplicate_user_email(self):
        self.create_users()
        with self.assertRaises(Exception):
            User.create_user(
                username='user_188',
                email='test_1@example.com',
                password='password'
            )

    @use_test_database
    def test_create_duplicate_user_username(self):
        self.create_users()
        with self.assertRaises(Exception):
            User.create_user(
                username='user_1',
                email='test_188@example.com',
                password='password'
            )


class TestResources(TestCase):
    def setUp(self):
        self.app = app.test_client()

        self.data = {
            "name": "Walk the dog"
        }

    @use_test_database
    def test_post_task(self):
        response = self.app.post(
            path='/api/v1/todos',
            data=json.dumps(self.data),
            content_type='application/json')
        self.assertEqual(response.status_code, 201)

    @use_test_database
    def test_get_todos(self):
        response = self.app.get(
            path='/api/v1/todos',
            content_type='application/json')
        self.assertEqual(response.status_code, 200)
