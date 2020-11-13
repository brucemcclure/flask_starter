from flask import Flask, jsonify                            # Importing the flask class
from marshmallow.exceptions import ValidationError
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager                       # import the jwt manager

db = SQLAlchemy()                                               # Make a new instance of the SQL ALchemy
ma = Marshmallow()                                              # Make a new instance of the MArshmallow
bcrypt = Bcrypt()                                               # Make a new instance of Bcrypt
jwt = JWTManager()                                              # Make a new instance of the JWT manager


# The factory pattern is where you create an object without exposing its creation logic.
# Basically the factory pattern uses a function to instantiate a new object and then returns that object from the function.

# Flask run, by default looks into main.py and runs creat_app automatically

def create_app():                                               # Flask convention for when you want to create an app in the factory pattern
    from dotenv import load_dotenv                              # This is the package used to set env varibles
    load_dotenv()                                               # Load the env variables

    app = Flask(__name__)                                       # Creating an app instnace from the flask class
    app.config.from_object("default_settings.app_config")       # Loads our configuration from defatult_settings.py

    #  These need the context of which 'app' it is currently using.
    # Therefore they need to be in the create_app function.
    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    from commands import db_commands                            # Import the db commands
    app.register_blueprint(db_commands)                         # Register the commands with app

    from controllers import registerable_controllers            # Importing the various controllers
    for controller in registerable_controllers:                 # Looping over the registerable_controllers and registering them
        app.register_blueprint(controller)

    @app.errorhandler(ValidationError)                          # Decorator for the ValidationError
    def handle_bad_request(error):                              # The handle bad request function inherits from the python error object
        return (jsonify(error.messages), 400)                   # Return the  error message in jason with a status of 400

    return app
