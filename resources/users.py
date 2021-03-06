import json

from flask import Blueprint, make_response
from flask_restful import Resource, Api, reqparse, fields, marshal, marshal_with, abort

import models
from auth import auth

user_fields = {
    'username': fields.String,
}

user_detail_fields = {
    'username': fields.String,
    'email': fields.String,
}


def user_or_404(user_id):
    """Return user from DB by ID, or error message if task does not exist."""
    try:
        user = models.User.get(models.User.id == user_id)
    except models.User.DoesNotExist:
        abort(404, message='User with ID {} does not exist'.format(user_id))
    else:
        return user


class UserList(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'username',
            required=True,
            help='No username provided',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'email',
            required=True,
            help='No email provided',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'password',
            required=True,
            help='No password provided',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'verify_password',
            required=True,
            help='No password verification provided',
            location=['form', 'json']
        )
        super().__init__()

    @auth.login_required
    def get(self):
        """Return a list of registered users."""
        users = [marshal(user, user_fields) for user in models.User.select()]
        return {'users': users}

    def post(self):
        """Add a new user."""
        args = self.reqparse.parse_args()
        if args.get('password') == args.get('verify_password'):
            user = models.User.create_user(**args)
            return marshal(user, user_fields), 201
        return make_response(json.dumps({'error': "Password and password verification do not match"}), 400)


class User(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()

    @marshal_with(user_detail_fields)
    @auth.login_required
    def get(self, id):
        """Return the username and email for the selected userID"""
        return user_or_404(id)


users_api = Blueprint('resources.users', __name__)
api = Api(users_api)

api.add_resource(
    UserList,
    '/users',
    endpoint='users'
)

api.add_resource(
    User,
    '/users/<int:id>',
    endpoint='user'
)
