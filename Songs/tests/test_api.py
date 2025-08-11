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
                    })

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
