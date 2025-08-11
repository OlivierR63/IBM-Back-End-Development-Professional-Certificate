# tests/conftest.py
import pytest
import os
import json   # To load songs.json
from pymongo import MongoClient
from pymongo.database import Database   # Imports this type for type hinting

# Imports the create_app function from the backend package, instead
# of the app instance directly.
from backend import create_app


# --- Fixtures for the test database ---
@pytest.fixture(scope="module")
def test_db() -> Database:
    """
    Configures and returns a connection to a distinct MongoDB database
    for testing. The database is created at the beginning of the test module
    and dropped at the end.
    """
    mongodb_service = os.environ.get('MONGODB_SERVICE', 'localhost')
    mongodb_username = os.environ.get('MONGODB_USERNAME')
    mongodb_password = os.environ.get('MONGODB_PASSWORD')
    mongodb_port = os.environ.get('MONGODB_PORT', '27017')

    if mongodb_username and mongodb_password:
        url = f"mongodb://{mongodb_username}:{mongodb_password}"
        url += f"@{mongodb_service}:{mongodb_port}/"
    else:
        url = f"mongodb://{mongodb_service}:{mongodb_port}/"

    print(f"\n[Pytest Fixture] Connecting to test MongoDB at: {url}")

    client = MongoClient(url)
    test_db_name = "test_songs_db"   # Separates database name for tests
    db = client[test_db_name]

    # Makes sure the database is empty when the test module starts
    client.drop_database(db)
    print(f"[Pytest Fixture] Dropped existing test database: {test_db_name}")

    yield db   # Provides the Database object to Pytest

    # Teardown after all module tests execute
    print(f"[Pytest Fixture] Cleaning up test database: {test_db_name}")
    client.drop_database(db)
    client.close()
    print("[Pytest Fixture] Test database cleaned up and client closed.")


@pytest.fixture(scope="function")
def test_collection(test_db):
    """
    Configures and returns a test collection, populated with initial data.
    The collection is cleared (emptied) after each test to ensure a fresh state
    """
    collection_name = "songs"
    collection = test_db[collection_name]

    # Path to songs.json
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_path = os.path.join(SITE_ROOT, "..", "backend", "data", "songs.json")

    try:
        with open(json_path, 'r') as f:
            songs_list = json.load(f)
        if songs_list:
            collection.insert_many(songs_list)
        str_msg = f"[Pytest Fixture] Inserted {len(songs_list)} documents "
        str_msg += f"into {collection_name}"
        print(str_msg)
    except FileNotFoundError:
        str_msg = f"songs.json not found at {json_path}. "
        str_msg += "Cannot populate test collection."
        pytest.fail(str_msg)
    except Exception as e:
        pytest.fail(f"Error loading songs.json or inserting data: {e}")

    yield collection  # Yields the populated collection to the test

    # Cleans up after each test
    print(f"[Pytest Fixture] Dropping test collection: {collection_name}")
    collection.drop()


# --- Test Application Fixture ---

@pytest.fixture(scope="module")
def app(test_db):   # The 'app' fixture depends on the 'test_db' fixture
    """
    Generates a Flask application instance configured for testing.
    The test database is then injected into this application instance.
    """
    # Uses the create_app function from backend/__init__.py
    app_instance = create_app({"TESTING": True})

    # Injects the test database into the application instance.
    # This step is critical for maintaining test isolation.
    app_instance.db = test_db

    yield app_instance


@pytest.fixture()
def client(app):   # The 'client' fixture depends on the new 'app' fixture.
    """
    Provides a Flask test client for making HTTP requests
    on the test application instance.
    """
    return app.test_client()


@pytest.fixture()
def picture():
    """
    Fixture to provide a test 'picture' object.
    """
    picture = {
        "id": 200,
        "pic_url": "http://dummyimage.com/230x100.png/dddddd/000000",
        "event_country": "United States",
        "event_state": "California",
        "event_city": "Fremont",
        "event_date": "11/2/2030"
    }
    return dict(picture)
