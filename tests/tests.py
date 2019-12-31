from peewee import *
import json
import unittest

from models import Todo, User

from app import app

MODELS = [User, Todo]

db = SqliteDatabase('todo.sqlite')


class TodoTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.app.testing = True
        self.client = app.test_client()
        self.user_data = {
            "username": 'user_1',
            "email": 'user_1@example.com',
            "password": 'password',
            "verify_password": 'password'
        }
        self.user_creds = {
            "username": 'user_1',
            "email": 'user_1@example.com',
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
            username='tester',
            email='tester@test.com',
            password='password'
        )
        self.token = self.test_user_1.generate_auth_token()

    def format_token(self):
        return "token " + self.token.decode('ascii')

    def tearDown(self):
        pass
        db.drop_tables(MODELS)
        db.close()

    def test_create_user(self):
        # create user via api
        response = self.client.post(
            path='/api/v1/users',
            data=json.dumps(self.user_data),
            content_type='application/json')
        self.assertEqual(response.status_code, 201)

    def test_login_user(self):
        # login user via api
        response = self.client.post(
            path='/login',
            data=json.dumps(self.user_creds),
            content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_todo_resources(self):
        # post task via api
        token = self.format_token()
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
        response = self.client.get(
            path='/api/v1/todos/{}'.format(79489),
            headers={
                'Content-Type': 'application/json',
                'Authorization': token
            })
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'Todo 79489 does not exist', response.data)

        #  edit task via api
        response = self.client.put(
            path='/api/v1/todos/{}'.format(todo.id),
            data=json.dumps(self.new_data),
            headers={
                'Content-Type': 'application/json',
                'Authorization': token
            })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Feed the cat', response.data)

        #  delete task via api
        response = self.client.delete(
            path='/api/v1/todos/{}'.format(todo.id),
            headers={
                'Content-Type': 'application/json',
                'Authorization': token
            })
        self.assertEqual(response.status_code, 204)

        # delete nonexistent task (403) via api
        response = self.client.delete(
            path='/api/v1/todos/{}'.format(79489),
            headers={
                'Content-Type': 'application/json',
                'Authorization': token
            })
        self.assertEqual(response.status_code, 403)

    def test_post_api(self):
        # create user via api
        response = self.client.post(
            path='/api/v1/users',
            data=json.dumps(self.user_data),
            content_type='application/json')
        self.assertEqual(response.status_code, 201)


if __name__ == '__main__':
    unittest.main()
