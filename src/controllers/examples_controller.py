from models.Example import Example                                  # This is the module that will communicate with the example table
from models.User import User                                        # This is the module that will communicate with the user table
from main import db                                                 # Db connection
from flask import Blueprint, request, jsonify, abort                # We need to be able to create a blueprint and retrieve and send back data
from schemas.ExampleSchema import examples_schema, example_schema   # Importing the serialization module
from flask_jwt_extended import jwt_required, get_jwt_identity       # This function will check if we have a JWT sent along with our request or not
from services.auth_service import verify_user
from sqlalchemy.orm import joinedload

examples = Blueprint("examples", __name__, url_prefix="/examples")  # Creating the blueprint and specifying the url_prefix


# These are examples of raw sql crud. They will be replaced with a ORM soon

# Return all examples
@examples.route("/", methods=["GET"])
def example_index():
    examples = Example.query.options(joinedload("user")).all()    # Using the Example model to fetch all the examples with the query method
    return jsonify(examples_schema.dump(examples))                # Return the data in the form of JSON


# Create a new example
@examples.route("/", methods=["POST"])                              # Define the route and method
@jwt_required
@verify_user
def example_create(user=None):                                      # Define the create function. user=none to use the decorator

    example_fieds = example_schema.load(request.json)               # Deserializing the json into something that can be used

    new_example = Example()                                         # Creating a new instance of example
    new_example.title = example_fieds["title"]                      # Update the title

    user.examples.append(new_example)                               # Add this example to the the user who created it
    db.session.commit()                                             # Commit the transaction
    return jsonify(example_schema.dump(new_example))                # Return the json format of the example


# Return a single example
@examples.route("/<int:id>", methods=["GET"])                       # Define the route and method
def example_show(id):                                               # Define the show function, , takes the id as an argument
    example = Example.query.get(id)                                 # Using the Example model to fetch one example with a specific id using the query method
    return jsonify(example_schema.dump(example))                    # Return the Example in the form of JSON


# Update a example
@examples.route("/<int:id>", methods=["PUT", "PATCH"])              # Define the route and method
@jwt_required
@verify_user
def example_update(id, user=None):                                  # Define the update function, takes the id as an argument. user=none to use the decorator
    example_fields = example_schema.load(request.json)              # Deserializing the json into something that can be used

    examples = Example.query.filter_by(id=id, user_id=user.id)      # Check if the user owns that example

    if examples.count() != 1:                                       # Raise error if the user is not authorized
        return abort(401, description="Unauthorized to update this example")

    examples.update(example_fields)                                 # Update examples with the new data
    db.session.commit()                                             # Commit the transaction to the DB
    return jsonify(example_schema.dump(examples[0]))                # Return the data

# Delete a example


@examples.route("/<int:id>", methods=["DELETE"])                    # Define the route and method
@jwt_required
@verify_user
def example_delete(id, user=None):                                  # Define the update function, takes the id as an argument. user=none to use the decorator

    example = Example.query.filter_by(id=id, user_id=user.id).first()  # Check if the user owns that example

    if not example:                                                 # If no example exisits then
        return abort(400)

    db.session.delete(example)                                      # Delete the example
    db.session.commit()                                             # Commit the transaction to the database
    return jsonify(example_schema.dump(example))                    # Return the data in the form of json
