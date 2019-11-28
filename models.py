import datetime

from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer,
                          BadSignature, SignatureExpired)
from peewee import *

import config

DATABASE = SqliteDatabase('todo.sqlite')


class Todo(Model):
    name = CharField()
    edited = BooleanField(default=False)
    completed = BooleanField(default=False)

    class Meta:
        database = DATABASE


def initialize():
    DATABASE.connect(reuse_if_open=True)
    DATABASE.create_tables([Todo], safe=True)
    DATABASE.close()
