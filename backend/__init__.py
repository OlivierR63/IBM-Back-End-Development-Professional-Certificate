# backend/__init__.py
import os
import json
from flask import Flask
from pymongo import MongoClient
from pymongo.errors import OperationFailure
from .routes import register_routes


def create_app(test_config=None):
    """
    Creates and configures a new Flask application instance.
    Can take a test_config dictionary to configure the application for testing
    """
    app = Flask(__name__, instance_relative_config=True)

    # Default configuration
    app.config.from_mapping(
        SECRET_KEY='dev',
        # Additional default configurations can be placed here
    )

    if test_config is None:
        # For development/production environments, loads the instance
        # configuration file if available.
        # If the file does not exist, the parameter silent=True
        # make Flask ignore this call.
        app.config.from_pyfile('config.py', silent=True)
    else:
        # Applies the given test configuration to the test environment
        app.config.from_mapping(test_config)

    # Makes sure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Initializing the MongoDB database connection
    # These environment variables must be set for the production environment
    mongodb_service = os.environ.get('MONGODB_SERVICE', 'localhost')
    mongodb_username = os.environ.get('MONGODB_USERNAME')
    mongodb_password = os.environ.get('MONGODB_PASSWORD')

    # The default port for MongoDB is 27017
    mongodb_port = os.environ.get('MONGODB_PORT', '27017')

    # Determines the database name to use
    # When in test mode, the test_db fixture injects its own database,
    # replacing the default.
    # 'songs' is the Default name for production
    db_name = os.environ.get('MONGODB_DATABASE', 'songs')

    if test_config and test_config.get("TESTING"):
        # In test mode, the test_db fixture will be injected.
        # To prevent double connection or conflict,
        # the app.db attribute will just be "prepared" to be replaced.
        # Otherwise, the connection is ensured within the fixture.
        msg_str = "Application in test mode, DB will be injected by Pytest."
        app.logger.info(msg_str)
        app.db = None  # Will be replaced by the fixture test_db
    else:
        # Connection for the production/development environment
        if mongodb_username and mongodb_password:
            url = f"mongodb://{mongodb_username}:{mongodb_password}"
            url += f"@{mongodb_service}:{mongodb_port}/"
        else:
            url = f"mongodb://{mongodb_service}:{mongodb_port}/"

        app.logger.info(f"Connecting to production MongoDB at: {url}")
        try:
            client = MongoClient(url)
            app.db = client[db_name]  # The production/development database
            app.logger.info(f"Connected to MongoDB database: {db_name}")

            # Initial data cleanup / reloading for the development environment
            # WARNING: This is EXTREMELY DANGEROUS IN PRODUCTION!
            # In production, NEVER clear and reload the DB on every startup.
            # This is a dev practice to ensure fresh data.
            SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
            json_url = os.path.join(SITE_ROOT, "data", "songs.json")
            try:
                with open(json_url, 'r') as f:
                    songs_list: list = json.load(f)

                # Load only if the collection is empty
                if app.db.songs.count_documents({}) == 0:
                    app.db.songs.insert_many(songs_list)
                    msg_str = f"Inserted {len(songs_list)} initial songs "
                    msg_str += "into production DB."
                    app.logger.info(msg_str)

                else:
                    msg_str = "Production DB already contains songs, "
                    msg_str += "skipping initial load."
                    app.logger.info(msg_str)

            except FileNotFoundError:
                msg_str = f"songs.json not found at {json_url}. "
                msg_str += "No initial songs loaded in production DB."
                app.logger.warning(msg_str)

            except Exception as e:
                msg_str = "Error loading initial songs data "
                msg_str += f"for production DB: {e}"
                app.logger.error(msg_str)

        except OperationFailure as e:
            app.logger.critical(f"MongoDB Authentication error: {str(e)}")
            # For a real application, you might want to handle this
            # more gracefully.
            # sys.exit(1) or raise a custom exception.
            raise e
        except Exception as e:
            app.logger.critical(f"Failed to connect to MongoDB: {str(e)}")
            raise e

    # Calls the function register_routes to link the routes
    # with the 'app' instance
    register_routes(app)

    return app


# Application instance for the production/development environment
# This is the instance that Gunicorn or 'flask run' will use by default.
app = create_app()
