from peewee import *
import json
import unittest

from models import Todo, User

from app import app

MODELS = [User, Todo]

db = SqliteDatabase('todo.sqlite')


class TodoTestCase(unittest.TestCase):
    def setUp(self):
        """Set up the unit tests."""
        self.app = app
        self.app.testing = True
        self.client = app.test_client()
        self.user_data = {
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
        db.bind(MODELS, bind_refs=False, bind_backrefs=False)
        db.connect()
        db.create_tables(MODELS)

        self.test_user_1 = User.create_user(
            username='tester_1',
            email='tester_1@test.com',
            password='password'
        )

        self.test_user_2 = User.create_user(
            username='tester_2',
            email='tester_2@test.com',
            password='password'
        )

    def format_token(self, user):
        """Return the user token in a header-friendly format."""
        self.token = user.generate_auth_token()
        return "token " + self.token.decode('ascii')

    def tearDown(self):
        db.drop_tables(MODELS)
        db.close()

    def test_create_user(self):
        # create user via api
        response = self.client.post(
            path='/api/v1/users',
            data=json.dumps(self.user_data),
            content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertIn(b'username": "user_1', response.data)

    def test_todo_resources(self):
        # post task via api
        token = self.format_token(self.test_user_1)
        response = self.client.post(
            path='/api/v1/todos',
            data=json.dumps(self.data),
            headers={
                'Content-Type': 'application/json',
                'Authorization': token
            })
        self.assertEqual(response.status_code, 201)

        #  get all tasks via api
        todo = Todo.get(name='Walk the dog in the park')
        response = self.client.get(
            path='/api/v1/todos',
            headers={
                'Content-Type': 'application/json',
            })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Walk the dog in the park', response.data)

        #  get single task via api
        response = self.client.get(
            path='/api/v1/todos/{}'.format(todo.id),
            headers={
                'Content-Type': 'application/json',
                'Authorization': token
            })
        self.assertEqual(response.status_code, 200)

        #  get single (404) via api
        token = self.format_token(self.test_user_1)
        response = self.client.get(
            path='/api/v1/todos/{}'.format(79489),
            headers={
                'Content-Type': 'application/json',
                'Authorization': token
            })
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'Todo 79489 does not exist', response.data)

        #  edit task not owned by current user via api
        token = self.format_token(self.test_user_2)
        response = self.client.put(
            path='/api/v1/todos/{}'.format(todo.id),
            data=json.dumps(self.new_data),
            headers={
                'Content-Type': 'application/json',
                'Authorization': token
            })
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Only the task owner can edit this task', response.data)

        #  edit task via api
        token = self.format_token(self.test_user_1)
        response = self.client.put(
            path='/api/v1/todos/{}'.format(todo.id),
            data=json.dumps(self.new_data),
            headers={
                'Content-Type': 'application/json',
                'Authorization': token
            })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Feed the cat', response.data)

        #  delete task not owned by current user via api
        token = self.format_token(self.test_user_2)
        response = self.client.delete(
            path='/api/v1/todos/{}'.format(todo.id),
            headers={
                'Content-Type': 'application/json',
                'Authorization': token
            })
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Only the task owner can delete this task', response.data)

        #  delete task via api
        token = self.format_token(self.test_user_1)
        response = self.client.delete(
            path='/api/v1/todos/{}'.format(todo.id),
            headers={
                'Content-Type': 'application/json',
                'Authorization': token
            })
        self.assertEqual(response.status_code, 204)

        # delete nonexistent task (403) via api
        token = self.format_token(self.test_user_1)
        response = self.client.delete(
            path='/api/v1/todos/{}'.format(79489),
            headers={
                'Content-Type': 'application/json',
                'Authorization': token
            })
        self.assertEqual(response.status_code, 403)


if __name__ == '__main__':
    unittest.main()
