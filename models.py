import datetime

from peewee import *

db = SqliteDatabase('todo.sqlite')

class Todo(Model):
    """Hold all the To-do tasks."""
    name = CharField()
    edited = BooleanField(default=False)
    completed = BooleanField(default=False)
    created_at = DateTimeField(default=datetime.datetime.now)
    updated_at = DateTimeField(null=True, default=None)

    class Meta:
        database = db


def initialize():
    db.connect(reuse_if_open=True)
    db.create_tables([Todo], safe=True)
    db.close()
