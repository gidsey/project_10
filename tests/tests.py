from peewee import SqliteDatabase
import json
import unittest
from app import app
from models import User, Todo

MODELS = [User, Todo]
# use an in-memory SQLite for tests.
test_db = SqliteDatabase(':memory:')


class TodoTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.app.testing = True
        self.client = app.test_client()
        self.user = {
                "username": 'user_1',
                "email": 'user_1@example.com',
                "password": 'password',
                "verify_password": 'password'
        }
        self.data = {
            "name": "Walk the dog in the park"
        }
        self.new_data = {
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
        test_db.drop_tables(MODELS)
        test_db.close()

    def test_todo_api(self):
        # CREATE USER
        resp = self.client.post(
            path='/api/v1/users',
            data=json.dumps(self.user),
            content_type='application/json')
        self.assertEqual(resp.status_code, 201)

        #  POST
        resp = self.client.post(
            path='/api/v1/todos',
            data=json.dumps(self.data),
            content_type='application/json')
        self.assertEqual(resp.status_code, 201)
        todo = Todo.get(name='Walk the dog in the park')

        #  GET ALL
        resp = self.client.get(
            path='/api/v1/todos',
            content_type='application/json')
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b'Walk the dog in the park', resp.data)

        #  GET SINGLE
        resp = self.client.get(
            path='/api/v1/todos/{}'.format(todo.id),
            content_type='application/json')
        self.assertEqual(resp.status_code, 200)

        #  GET SINGLE (404)
        resp = self.client.get(
            path='/api/v1/todos/{}'.format(79489),
            content_type='application/json')
        self.assertEqual(resp.status_code, 404)
        self.assertIn(b'Todo 79489 does not exist', resp.data)

        #  EDIT TASK
        resp = self.client.put(
            path='/api/v1/todos/{}'.format(todo.id),
            data=json.dumps(self.new_data),
            content_type='application/json')
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b'Feed the cat', resp.data)

        #  DELETE TASK
        resp = self.client.delete(
            path='/api/v1/todos/{}'.format(todo.id))
        self.assertEqual(resp.status_code, 204)

        #  DELETE TASK (403)
        resp = self.client.delete(
            path='/api/v1/todos/{}'.format(79489))
        self.assertEqual(resp.status_code, 403)


if __name__ == '__main__':
    unittest.main()
