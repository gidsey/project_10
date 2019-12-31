import json
import datetime

from flask import Blueprint, url_for, make_response, g

from flask_restful import Resource, Api, reqparse, fields, marshal, marshal_with, abort

from auth import auth

import models


todo_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'edited': fields.Boolean,
    'completed': fields.Boolean,
    'created_at': fields.String,
    'updated_at': fields.String,
    'created_by': fields.String,
}


def todo_or_404(todo_id):
    """Return task from DB by ID, or error message if task does not exist."""
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
        """Return a list of tasks."""
        todos = [marshal(todo, todo_fields) for todo in models.Todo.select()]
        return todos

    @marshal_with(todo_fields)
    @auth.login_required
    def post(self):
        """Post a new task and assign it to the current user"""
        args = self.reqparse.parse_args()
        todo = models.Todo.create(
            created_by=g.user,
            **args
        )
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
            'updated_at',
            required=True,
            help='No updated_at time provided',
            location=['form', 'json'],
        )
        super().__init__()

    @marshal_with(todo_fields)
    def get(self, id):
        """Return details of a single task."""
        return todo_or_404(id)

    @marshal_with(todo_fields)
    @auth.login_required
    def put(self, id):
        """
        Allow task owners to edit existing tasks.
        Prevent other users from editing tasks that do not belong to them.
        """
        task_owner = models.Todo.get(models.Todo.id == id).created_by
        if g.user != task_owner:
            abort(400, message='Only the task owner can edit this task')
        else:
            args = self.reqparse.parse_args()
            args.edited = False
            args.updated_at = datetime.datetime.now()
            query = models.Todo.update(**args).where(models.Todo.id == id)
            query.execute()
            todo = todo_or_404(id)
            return todo, 200, {'location': url_for('resources.todos.todo', id=todo.id)}

    @auth.login_required
    def delete(self, id):
        try:
            task_owner = models.Todo.get(models.Todo.id == id).created_by
        except models.Todo.DoesNotExist:
            return make_response(json.dumps({'error': "That TODO does not exist"}), 403)
        if g.user != task_owner:
            abort(400, message='Only the task owner can delete this task')
        else:
            todo = models.Todo.get(models.Todo.id == id)
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