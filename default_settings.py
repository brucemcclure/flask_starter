import os  # This is the OS package which is used to retrieve environment variables

# Parent class called config. All other classes inherit from it.


class Config(object):
    # connect to postgres+using psycopg2://username:password@localhost:port/name_of_db
    SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg2://app:{os.getenv('DB_PASSWORD')}@localhost:5432/library_api"
    JWT_SECRET_KEY = "Mr quackers"
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # If not needed then this should be disabled because it uses extra memory.

    @property
    def SQLALCHEMY_DATABASE_URI(self):         # This is a function that will be used for all envs
        value = os.environ.get("DB_URI")       # Retriieve the db uri from the .env file
        if not value:
            raise ValueError("DB_URI is not set")
        return value


class DevelopmentConfig(Config):  # Inherits from config
    DEBUG = True                 # Adds in the debugging mode for development


class ProductionConfig(Config):  # Inherits from config
    @property
    def JWT_SECRET_KEY(self):
        value = os.environ.get("JWT_SECRET_KEY")
        if not value:
            raise ValueError("JWT Secret Key is not set")

        return value


class TestingConfig(Config):  # Inherits from config
    TESTING = True           # Adds in the testing env-var


environment = os.environ.get("FLASK_ENV")  # Retrieve the the flask env variable

if environment == "production":        # If the flask env variable is production
    app_config = ProductionConfig()    # Then use the production config
elif environment == "testing":         # If the flask env variable is testing
    app_config = TestingConfig()       # Then use the testing config
else:
    app_config = DevelopmentConfig()   # Else use the development config
