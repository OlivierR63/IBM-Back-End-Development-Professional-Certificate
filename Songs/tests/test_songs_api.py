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


def test_health(client):
    res = client.get("/health")
    assert res.status_code == 200


def test_count(client, test_collection):
    res = client.get('/count')
    # Parses the response data to get the count
    data = res.get_json()
    assert data['count'] == 20  # Assuming the response is {"count": 20}
    assert res.status_code == 200


def test_get_all_songs(client, test_collection):
    res = client.get('/song')
    assert res.status_code == 200
    data = res.get_json()
    assert 'songs' in data.keys()
    assert isinstance(data['songs'], list)
    assert len(data['songs']) > 0
    for song in data['songs']:
        assert isinstance(song, dict)
        assert 'id' in song
        assert 'title' in song
        assert 'lyrics' in song
        assert '_id' in song


def test_get_song_by_id_success(client, test_collection):
    res = client.get('/song/1')
    assert res.status_code == 200
    song_data = res.get_json()
    assert isinstance(song_data, dict)
    assert song_data['id'] == 1
    assert 'title' in song_data


def test_get_song_by_id_not_found(client, test_collection):
    res = client.get('/song/99999')
    assert res.status_code == 404
    assert res.json['message'] == "ERROR: song whose id is 99999 not found"


# No need for test_collection if the DB is not queried
def test_get_song_by_id_invalid_id(client):
    res = client.get('/song/0')
    assert res.status_code == 400
    msg_str = "ERROR: ID must be a positive integer. Its actual value is 0"
    assert res.json['message'] == msg_str

    res = client.get('/song/-5')
    assert res.status_code == 400
    msg_str = "ERROR: ID must be a positive integer. Its actual value is -5"
    assert res.json['message'] == msg_str

    res = client.get('/song/xyz')
    assert res.status_code == 400
    msg_str = "ERROR: Invalid ID format. Its actual value is 'xyz'"
    assert res.json['message'] == msg_str


def test_create_song_success(client, test_collection):
    new_song = {
        "id": 21,
        "title": "New Test Song",
        "artist": "New Test Artist",
        "lyrics": "New test lyrics."
    }
    res = client.post('/song', json=new_song)
    assert res.status_code == 201
    response_data = res.get_json()
    assert 'inserted_id' in response_data

    # Checks directly in the test collection
    assert test_collection.find_one({'id': 21}) is not None


def test_create_song_already_exists(client, test_collection):
    # ID 1 is already in songs.json, so it should exist in test_collection
    existing_song_data = {
        "id": 1,
        "title": "Existing Song Title",
        "artist": "Existing Artist",
        "lyrics": "Some lyrics."
    }
    res = client.post('/song', json=existing_song_data)
    assert res.status_code == 302
    assert res.json['message'] == "song with id 1 already present"


def test_create_song_no_data(client):
    # or simply client.post('/song') if the body is truly empty
    res = client.post('/song', json={})
    assert res.status_code == 400
    assert res.json['message'] == "ERROR: Request data not found"


def test_update_song_success(client, test_collection):
    updated_data = {
        "title": "Updated Test Song Title",
        "artist": "Updated Artist Name"
    }

    # Updates the song with ID 1
    res = client.put('/song/1', json=updated_data)
    assert res.status_code in [200, 201]
    response_data = res.get_json()
    assert response_data['id'] == 1
    assert response_data['title'] == "Updated Test Song Title"

    # Verifies the update directly in the test collection
    updated_in_db = test_collection.find_one({'id': 1})
    assert updated_in_db['title'] == "Updated Test Song Title"


def test_update_song_not_found(client, test_collection):
    updated_data = {"title": "Non Existent Song"}
    res = client.put('/song/99999', json=updated_data)
    assert res.status_code == 404
    assert res.json['message'] == "Song not found"


def test_update_song_invalid_id(client):
    updated_data = {"title": "Invalid ID Song"}
    res = client.put('/song/0', json=updated_data)
    assert res.status_code == 400
    msg_str = "ERROR: ID must be a positive integer. Its actual value is 0"
    assert res.json['message'] == msg_str

    res = client.put('/song/-5', json=updated_data)
    assert res.status_code == 400
    msg_str = "ERROR: ID must be a positive integer. Its actual value is -5"
    assert res.json['message'] == msg_str

    res = client.put('/song/xyz', json=updated_data)
    assert res.status_code == 400
    msg_str = "ERROR: Invalid ID format. Its actual value is 'xyz'"
    assert res.json['message'] == msg_str


def test_delete_song_success(client, test_collection):
    # Creates a song to be deleted for this specific test
    temp_song_id = 100
    client.post('/song',
                json={
                        "id": temp_song_id,
                        "title": "Temp Delete",
                        "artist": "Temp",
                        "lyrics": "Temp"
                      }
                )

    res = client.delete(f'/song/{temp_song_id}')
    assert res.status_code == 204

    # Checks that it is no longer in the test collection
    assert test_collection.find_one({'id': temp_song_id}) is None


def test_delete_song_not_found(client, test_collection):
    res = client.delete('/song/99999')
    assert res.status_code == 404
    assert res.json['message'] == "Song not found"


def test_delete_song_invalid_id(client):
    res = client.delete('/song/0')
    assert res.status_code == 400
    str_msg = "ERROR: ID must be a positive integer. Its value is 0"
    assert res.json['message'] == str_msg

    res = client.delete('/song/-5')
    assert res.status_code == 400
    str_msg = "ERROR: ID must be a positive integer. Its value is -5"
    assert res.json['message'] == str_msg

    res = client.delete('/song/xyz')
    assert res.status_code == 400
    str_msg = "ERROR: Invalid ID format. Its actual value is 'xyz'"
    assert res.json['message'] == str_msg
