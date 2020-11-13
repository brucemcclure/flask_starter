from main import ma                          # Importing the instnace of ma, which has app registered with it.
from models.Example import Example                 # Importing the model that handles the example database.
from schemas.UserSchema import UserSchema    # Importing the user schema
from marshmallow.validate import Length      # This is the validator module in marshmallow


# Because we are using the auto schema marshmello will auto update the schema when we change the example model
class ExampleSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Example

    title = ma.String(required=True, validate=Length(min=1))        # This is declaring a required data type on the title column
    user = ma.Nested(UserSchema)                                    # Each example must have a user


example_schema = ExampleSchema()                  # How you serilaize and deserialize one object.
examples_schema = ExampleSchema(many=True)      # How you serilaize and deserialize many objects.
