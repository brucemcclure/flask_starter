from main import ma                                                 # This is the marshmellow object
from models.User import User                                        # Importign the USer model
from marshmallow.validate import Length                             # Import the length class that will allow us to validate the length of the string


class UserSchema(ma.SQLAlchemyAutoSchema):                          # Inherits from the AutoSchema so it gets csome configuration from the Model
    class Meta:
        model = User
        load_only = ["password"]                                    # This line ensures the hash is never nent back to the user

    email = ma.String(required=True, validate=Length(min=4))        # The email is required and must be at least 4 chars long
    password = ma.String(required=True, validate=Length(min=6))     # The password is required and must be at least 6 chars long because cyber security


user_schema = UserSchema()                                          # Schema for single users
users_schema = UserSchema(many=True)                                # Schema for multiple users because reasons
