from flask import Blueprint, url_for

from flask_restful import Resource, Api, reqparse, inputs, fields, marshal, marshal_with, abort

import models

todo_fields = {
    'name': fields.String,
}


class TodoList(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'name',
            required=True,
            help='No name provided',
            location=['form', 'json']
        )
        super().__init__()

    def get(self):
        todos = [marshal(todo, todo_fields) for todo in models.Todo.select()]
        # print(todos)
        return todos

    @marshal_with(todo_fields)
    def post(self):
        args = self.reqparse.parse_args()
        todo = models.Todo.create(**args)
        return 201, {'location': url_for('resources.todos.todo', id=todo.id)}



todos_api = Blueprint('resources.todos', __name__)
api = Api(todos_api)

api.add_resource(
    TodoList,
    '/todos',
    endpoint='todos'
)
