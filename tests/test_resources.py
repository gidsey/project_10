import flask
from peewee import *

from functools import wraps
from unittest import TestCase
from models import User, Todo

import json
from app import app


MODELS = (User, Todo,)

db = SqliteDatabase(':memory:')


# Bind the given models to the db for the duration of wrapped block.
def use_test_database(fn):
    @wraps(fn)
    def inner(self):
        with db.bind_ctx(MODELS):
            db.create_tables(MODELS)
            try:
                fn(self)
            finally:
                db.drop_tables(MODELS)

    return inner



class TestResources(TestCase):

    def setUp(self):
        self.app = app
        app.config['TESTING'] = True
        self.client = app.test_client()


        self.data = {
            "name": "Walk the dog in the park"
        }
        self.new_data = {
            "name": "Feed the cat",
            "edited": True,
            "completed": False,
            "updated_at": "",
        }


    @use_test_database
    def test_post_todos(self):
        response = self.app.post(
            path='/api/v1/todos',
            data=json.dumps(self.data),
            content_type='application/json')
        self.assertEqual(response.status_code, 201)
        todo = Todo.get(name='Walk the dog in the park')

    @use_test_database
    def test_get_todos(self):
        response = self.app.get(
            path='/api/v1/todos',
            content_type='application/json')
        self.assertEqual(response.status_code, 200)
