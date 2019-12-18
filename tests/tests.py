from peewee import *
import json
import unittest

from models import Todo, User
from flask import g

from app import app

MODELS = [User, Todo]

db = SqliteDatabase('todo.sqlite')


class TodoTestCase(unittest.TestCase):
    @staticmethod
    def create_users(count=2):
        for i in range(count):
            User.create_user(
                username='user_{}'.format(i),
                email='test_{}@example.com'.format(i),
                password='password',
                verify_password='password'
            )

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

    def tearDown(self):
        pass
        db.drop_tables(MODELS)
        db.close()




    def test_todo_api(self):
        # CREATE USER
        response = self.client.post(
            path='/api/v1/users',
            data=json.dumps(self.user),
            content_type='application/json')
        self.assertEqual(response.status_code, 201)


        # LOGIN USER
        response = self.client.post(
            path='/login',
            data=json.dumps(self.user_creds),
            content_type='application/json')
        self.assertEqual(response.status_code, 200)

        # self.user = User.get(username='user_1')


        #  POST
        with app.app_context():
            self.user = User.get(username='user_1')
            # self.token = self.user.generate_auth_token()
            g.user = self.user
            token = self.user.generate_auth_token()
            print('g.user={}'.format(g.user))
            response = self.client.post(
                path='/api/v1/todos',
                data=json.dumps(self.data),
                headers={
                    'Content-Type': 'application/json',
                    'Authorization': token
                })
            self.assertEqual(response.status_code, 201)
            todo = Todo.get(name='Walk the dog in the park')

        # #  GET ALL
        # response = self.client.get(
        #     path='/api/v1/todos',
        #     content_type='application/json')
        # self.assertEqual(response.status_code, 200)
        # self.assertIn(b'Walk the dog in the park', response.data)
        #
        # #  GET SINGLE
        # response = self.client.get(
        #     path='/api/v1/todos/{}'.format(todo.id),
        #     content_type='application/json')
        # self.assertEqual(response.status_code, 200)
        #
        # #  GET SINGLE (404)
        # response = self.client.get(
        #     path='/api/v1/todos/{}'.format(79489),
        #     content_type='application/json')
        # self.assertEqual(response.status_code, 404)
        # self.assertIn(b'Todo 79489 does not exist', response.data)
        #
        # #  EDIT TASK
        # response = self.client.put(
        #     path='/api/v1/todos/{}'.format(todo.id),
        #     data=json.dumps(self.new_data),
        #     content_type='application/json')
        # self.assertEqual(response.status_code, 200)
        # self.assertIn(b'Feed the cat', response.data)
        #
        # #  DELETE TASK
        # response = self.client.delete(
        #     path='/api/v1/todos/{}'.format(todo.id))
        # self.assertEqual(response.status_code, 204)
        #
        # #  DELETE TASK (403)
        # response = self.client.delete(
        #     path='/api/v1/todos/{}'.format(79489))
        # self.assertEqual(response.status_code, 403)


if __name__ == '__main__':
    unittest.main()
