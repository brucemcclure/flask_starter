from models.User import User                                            # User model
from schemas.UserSchema import user_schema                              # User Schema
from main import db                                                     # Importing the db
from main import bcrypt                                                 # Importing bcrypt
from flask_jwt_extended import create_access_token                      # JWT management lib
from datetime import timedelta                                          # time delta function from the date - time standard library
from flask import Blueprint, request, jsonify, abort                    # Importing the Blueprint class from flask

auth = Blueprint('auth', __name__, url_prefix="/auth")                  # Creating the auth blueprint into a varaibale called auth


@auth.route("/register", methods=["POST"])                             # Register route
def auth_register():
    user_fields = user_schema.load(request.json)                       # Getting the fields form the user schema in json format
    user = User.query.filter_by(email=user_fields["email"]).first()    # Checking if the email sent through has already been registered

    if user:
        return abort(400, description="Email already registered")      # If the email is already in use then return this error

    user = User()                                                      # Create a new user object
    user.email = user_fields["email"]                                  # Assign the email to the user

    user.password = bcrypt.generate_password_hash(user_fields["password"]).decode("utf-8")  # Assign the password to the user

    db.session.add(user)                                               # Add the commited user to the session
    db.session.commit()                                                # Commit the session to the database

    return jsonify(user_schema.dump(user))                             # Return the user in JSON format


@auth.route("/login", methods=["POST"])                                # Login route
def auth_login():
    user_fields = user_schema.load(request.json)                       # Getting the fields for the user in json format

    user = User.query.filter_by(email=user_fields["email"]).first()    # Check if the user is registered with the app at all

    expiry = timedelta(days=1)                                         # The jwt will expire in 1 day
    access_token = create_access_token(identity=str(user.id), expires_delta=expiry)         # Creating the JWT
    if not user or not bcrypt.check_password_hash(user.password, user_fields["password"]):  # If the user is not registered, or the password is incorrect then raise this error.
        return abort(401, description="Incorrect username and password")

    return jsonify({"token": access_token})                            # Return the JWT
