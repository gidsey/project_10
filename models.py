import datetime

from peewee import *

DATABASE = SqliteDatabase('todo.sqlite')


class Todo(Model):
    """Hold all the To-do tasks."""
    name = CharField()
    edited = BooleanField(default=False)
    completed = BooleanField(default=False)
    created_at = DateTimeField(default=datetime.datetime.now)
    updated_at = DateTimeField(null=True, default=None)

    class Meta:
        database = DATABASE


def initialize():
    DATABASE.connect(reuse_if_open=True)
    DATABASE.create_tables([Todo], safe=True)
    DATABASE.close()
