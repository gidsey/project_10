from peewee import SqliteDatabase
import json
import unittest
from app import app
from models import Todo

MODELS = [Todo]
# use an in-memory SQLite for tests.
test_db = SqliteDatabase(':memory:')


class BaseTestCase(unittest.TestCase):
    def setUp(self):
        # Bind model classes to test db. Since we have a complete list of
        # all models, we do not need to recursively bind dependencies.
        test_db.bind(MODELS, bind_refs=False, bind_backrefs=False)

        test_db.connect()
        test_db.create_tables(MODELS)

    def tearDown(self):
        # Not strictly necessary since SQLite in-memory databases only live
        # for the duration of the connection, and in the next step we close
        # the connection...but a good practice all the same.
        test_db.drop_tables(MODELS)

        # Close connection to db.
        test_db.close()

    def test_post_todo(self):
        resp = self.client.post(
            path='/api/v1/todos',
            data=json.dumps(self.data),
            content_type='application/json')
        self.assertEqual(resp.status_code, 201)

    def test_get_all_todos(self):
        resp = self.client.get(
            path='/api/v1/todos',
            content_type='application/json')
        self.assertEqual(resp.status_code, 200)

    def test_get_single_todos(self):
        resp = self.client.get(
            path='/api/v1/todos/1',
            content_type='application/json')
        self.assertEqual(resp.status_code, 200)


if __name__ == '__main__':
    unittest.main()
