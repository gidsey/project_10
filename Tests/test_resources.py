# import json
# import unittest
#
# from app import app
# from models import Todo, db
# import config
# config.TestConfig.testing = True
#
#
# class TestModel(unittest.TestCase):
#     def setUp(self):
#         self.app = app
#         self.client = self.app.test_client()
#         self.app.testing = True
#         self.data = {
#             "name": "clean the house",
#         }
#
#     def test_post_todo(self):
#         resp = self.client.post(
#             path='/api/v1/todos',
#             data=json.dumps(self.data),
#             content_type='application/json')
#         self.assertEqual(resp.status_code, 201)
#
#     def test_get_all_todos(self):
#         resp = self.client.get(
#             path='/api/v1/todos',
#             content_type='application/json')
#         self.assertEqual(resp.status_code, 200)
#
#     def test_get_single_todos(self):
#         resp = self.client.get(
#             path='/api/v1/todos/1',
#             content_type='application/json')
#         self.assertEqual(resp.status_code, 200)
#
#
# if __name__ == '__main__':
#     unittest.main()
