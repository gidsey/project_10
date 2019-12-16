from peewee import *

from functools import wraps
from unittest import TestCase
from models import User, Todo
from forms import RegisterForm
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


class TestForms(TestCase):
    @use_test_database
    def test_register_form(self):
        with app.app_context():
                form_data = ({
                'username': 'tester',
                'email': 'test@test.com',
                'password': 'password',
                'verify_password': 'password',
            })

                form = RegisterForm(data=form_data)
                self.assertTrue(form.validate_on_submit())



