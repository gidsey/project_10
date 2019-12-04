from peewee import SqliteDatabase
import json
import unittest
from app import app
import models
import datetime

MODELS = [models.Todo]
# use an in-memory SQLite for tests.
test_db = SqliteDatabase(':memory:')


class BaseTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.app.testing = True
        self.client = app.test_client()
        self.data = {"name": "Walk the dog"}
        self.newdata = {
            "name": "Feed the cat",
            "edited": True,
            "completed": False,
            "updated_at": "",
        }
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

    def test_todo(self):
        #  POST
        resp = self.client.post(
            path='/api/v1/todos',
            data=json.dumps(self.data),
            content_type='application/json')
        self.assertEqual(resp.status_code, 201)
        todo = models.Todo.get(name='Walk the dog')

        #  GET ALL
        resp = self.client.get(
            path='/api/v1/todos',
            content_type='application/json')
        self.assertEqual(resp.status_code, 200)

        #  GET SINGLE
        resp = self.client.get(
            path='/api/v1/todos/{}'.format(todo.id),
            content_type='application/json')
        self.assertEqual(resp.status_code, 200)

        #  EDIT TASK
        resp = self.client.put(
            path='/api/v1/todos/{}'.format(todo.id),
            data=json.dumps(self.newdata),
            content_type='application/json')
        self.assertEqual(resp.status_code, 200)

        #  DELETE TASK
        resp = self.client.delete(
            path='/api/v1/todos/{}'.format(todo.id))
        self.assertEqual(resp.status_code, 204)


if __name__ == '__main__':
    unittest.main()
