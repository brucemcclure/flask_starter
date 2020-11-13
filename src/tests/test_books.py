import unittest                                     # This is the inbuilt python testing module
from main import create_app, db                     # This is the app from the factory pattern
from models.Example import Example                        # This is the module that will communicate with the example table

# Becasue the app is created in the factory pattern.
# The tests now run the app

# Hooks are different insert points in a functions lifecycle
# We call them fixtures in flask and there are 3 levels
# Module fixtures run before and after the module
# Class based fixtures run before and after every class
# Test based fixtures run before before and after every test

# The tests must run in isolation because we cant guarentee which tests run in which order.


class TestExamples(unittest.TestCase):                 # This is the Parent class that will test our examples module.
    @classmethod
    def setUp(cls):
        cls.app = create_app()                      # Crating an instance of our app
        cls.app_context = cls.app.app_context()     # Creating context for which the app is in. The tests run in parrallel therefore we need to keep track of which instance of app we are using
        cls.app_context.push()                      # Pushing context. Read the docs for mre
        cls.client = cls.app.test_client()          # Adding the test client to the client
        db.create_all()                             # Create all the
        runner = cls.app.test_cli_runner()
        runner.invoke(args=["db", "seed"])          # This seeds the db

    @classmethod
    def tearDown(cls):                              # We want to delete all the data
        db.session.remove()                         # Remove the session from the db
        db.drop_all()                               # Drop all tables
        cls.app_context.pop()                       # Remove the context of the app

    def test_example_index(self):
        response = self.client.get("/examples/")       # make a get request to the app the "/examples/" url, save it to a response object

        data = response.get_json()                  # jsonify the data

        self.assertEqual(response.status_code, 200)  # Checking if the response code is 200 you can make it a range 200-299 too
        self.assertIsInstance(data, list)           # Checking the data type of the response code

    def test_example_create(self):
        response = self.client.post("/examples/", json={
            "title": "This is a test"
        })

        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertTrue(bool("id" in data.keys()))
        example = Example.query.get(data["id"])
        self.assertIsNotNone(example)

    def test_example_delete(self):
        example = Example.query.first()
        response = self.client.delete(f"/examples/{example.id}")
        data = response.get_json()

        self.assertEqual(response.status_code, 200)

        example = Example.query.get(example.id)
        self.assertIsNone(example)
