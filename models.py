import datetime

from argon2 import PasswordHasher
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer,
                          BadSignature, SignatureExpired)

from peewee import *
import config

db = SqliteDatabase('todo.sqlite')
HASHER = PasswordHasher()


class User(Model):
    username = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField()

    class Meta:
        database = db

    @classmethod
    def create_user(cls, username, email, password, **kwargs):
        email = email.lower()
        try:
            cls.select().where(
                (cls.email == email) | (cls.username ** username)
            ).get()
        except cls.DoesNotExist:
            user = cls(username=username, email=email)
            user.password = user.set_password(password)
            user.save()
            return user
        else:
            raise Exception("User with that username or email already exists.")

    @staticmethod
    def verify_auth_token(token):
        serializer = Serializer(config.SECRET_KEY)
        try:
            data = serializer.loads(token)
        except (SignatureExpired, BadSignature):
            return None
        else:
            user = User.get(User.id == data['id'])
            return user

    @staticmethod
    def set_password(password):
        return HASHER.hash(password)

    def verify_password(self, password):
        return HASHER.verify(self.password, password)

    def generate_auth_token(self, expires=360000):
        serializer = Serializer(config.SECRET_KEY, expires_in=expires)
        return serializer.dumps({'id': self.id})


class Todo(Model):
    """Hold all the To-do tasks."""
    name = CharField()
    edited = BooleanField(default=False)
    completed = BooleanField(default=False)
    created_at = DateTimeField(default=datetime.datetime.now)
    updated_at = DateTimeField(null=True, default=None)
    user = ForeignKeyField(User, related_name='todo_set', on_delete='CASCADE')

    class Meta:
        database = db


def initialize():
    db.connect(reuse_if_open=True)
    db.create_tables([User, Todo], safe=True)
    db.close()
