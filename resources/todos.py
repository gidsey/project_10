import json

from flask import Blueprint, url_for, make_response

from flask_restful import Resource, Api, reqparse, fields, marshal, marshal_with, abort

import models

todo_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'edited': fields.Boolean,
    'completed': fields.Boolean,
    'created_at': fields.DateTime,
    'updated_at': fields.DateTime,
}


def todo_or_404(todo_id):
    try:
        todo = models.Todo.get(models.Todo.id == todo_id)
    except models.Todo.DoesNotExist:
        abort(404, message='Todo {} does not exist'.format(todo_id))
    else:
        return todo


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
        print(todos)
        return todos

    @marshal_with(todo_fields)
    def post(self):
        args = self.reqparse.parse_args()
        todo = models.Todo.create(**args)
        return todo, 201, {'location': url_for('resources.todos.todo', id=todo.id)}

class Todo(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'name',
            required=True,
            help='No name provided',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'edited',
            required=True,
            help='No edit state provided',
            location=['form', 'json'],
            type=bool
        )
        self.reqparse.add_argument(
            'completed',
            required=True,
            help='No completed state provided',
            location=['form', 'json'],
            type=bool
        )
        self.reqparse.add_argument(
            'created_at',
            required=True,
            help='No created_at time provided',
            location=['form', 'json'],
        )
        self.reqparse.add_argument(
            'updated_at',
            required=True,
            help='No updated_at time provided',
            location=['form', 'json'],
        )
        super().__init__()

    @marshal_with(todo_fields)
    def get(self, id):
        return todo_or_404(id)

    @marshal_with(todo_fields)
    def put(self, id):
        args = self.reqparse.parse_args()
        query = models.Todo.update(**args).where(models.Todo.id == id)
        query.execute()
        todo = todo_or_404(id)
        return {'name': todo.name}, 200, {'location': url_for('resources.todos.todo', id=todo.id)}


    def delete(self, id):
        try:
            todo = models.Todo.get(models.Todo.id == id)
        except models.Todo.DoesNotExsist():
            return make_response(json.dumps({'error': "That todo does not exist"}), 403)
        else:
            todo.delete_instance()
        return '', 204,


todos_api = Blueprint('resources.todos', __name__)
api = Api(todos_api)

api.add_resource(
    TodoList,
    '/todos',
    endpoint='todos'
)

api.add_resource(
    Todo,
    '/todos/<int:id>',
    endpoint='todo'
)