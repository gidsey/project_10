import unittest

from app import app

from app import models

from flask_fixtures import FixturesMixin

# Configure the app with the testing configuration
app.config.from_object('myapp.config.TestConfig')


# Make sure to inherit from the FixturesMixin class
class TestModel(unittest.TestCase, FixturesMixin):

    # Specify the fixtures file(s) you want to load.
    # Change the list below to ['authors.yaml'] if you created your fixtures
    # file using YAML instead of JSON.
    fixtures = ['todos.json']

    # Specify the Flask app and db we want to use for this set of tests
    app = app
    # db = db

    # Your tests go here

    def test_authors(self):
        todos = models.Todo.query.all()
        assert len(todos) == todos.query.count() == 1
        # assert len(todos[0].books) == 3



