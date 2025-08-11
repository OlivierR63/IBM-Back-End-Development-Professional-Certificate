import json
from flask import Flask, jsonify, request, make_response, abort, url_for, Response, current_app  # noqa; F401
from bson import json_util
from typing import Any, Tuple, Dict


def parse_json(data: Any) -> Any:
    """
    Converts MongoDB BSON-specific types within data to standard
    JSON-compatible Python types.

    Args:
        data (Any): The data containing BSON types to be parsed.

    Returns:
        Any: A Python object (dict, list, etc.) with BSON types converted
        to JSON-friendly formats.
    """
    return json.loads(json_util.dumps(data))


# Defines a function that takes a Flask instance as an input parameter and
# registers all the routes on it
def register_routes(app_instance: Flask):
    """
    Registers all API routes with the given Flask application instance.
    """

    ######################################################################
    # INSERT CODE HERE
    ######################################################################
    @app_instance.route('/health', methods=["GET"])
    def get_health() -> Tuple[Response, int]:
        """
        Checks the health status of the service.

        Returns:
            Tuple[Response, int]: A tuple containing a JSON response
            and an HTTP status code.
        """
        return {"status": "OK"}, 200

    @app_instance.route("/count", methods=["GET"])
    def get_count() -> Tuple[Response, int]:
        """
        Gets the total count of songs in the database.

        Returns:
            Tuple[Response, int]: A tuple containing a JSON response
            and an HTTP status code.
        """
        count = current_app.db.songs.count_documents({})
        return jsonify({"count": count}), 200

    @app_instance.route("/song", methods=["GET"])
    def get_songs() -> Tuple[Response, int]:
        """
        Retrieves all songs from the database.

        Returns:
            Tuple[Response, int]: A tuple containing a JSON response
            and an HTTP status code.
        """
        db_songs_list = list(current_app.db.songs.find({}))
        songs_json = json_util.dumps({"songs": db_songs_list})
        return Response(songs_json, mimetype='application/json')

    @app_instance.route("/song/<string:id_str>", methods=["GET"])
    def get_song_by_id(id_str: str) -> Tuple[Response, int]:
        """
        Retrieves a song by its ID.

        Args:
            id_str (str): The ID of the song to retrieve.

        Returns:
            Tuple[Response, int]: A tuple containing a JSON response
            and an HTTP status code.
        """
        try:
            id = int(id_str)
        except ValueError:
            message_str = "ERROR: Invalid ID format. "
            message_str += f"Its actual value is '{id_str}'"
            return jsonify({"message": message_str}), 400

        if id <= 0:
            message_str = "ERROR: ID must be a positive integer. "
            message_str += f"Its actual value is {id}"
            return jsonify({"message": message_str}), 400

        song_by_id = current_app.db.songs.find_one({'id': id})

        if (song_by_id is None):
            message_str = f"ERROR: song whose id is {id} not found"
            return jsonify({"message": message_str}), 404

        song_json = json_util.dumps(song_by_id)
        return Response(song_json, mimetype='application/json'), 200

    @app_instance.route("/song", methods=["POST"])
    def create_song() -> Tuple[Response, int]:
        """
        Creates a new song in the database.

        Returns:
            Tuple[Response, int]: A tuple containing a JSON response
            and an HTTP status code.
        """
        json_data = request.get_json()

        # Checks the existence of some JSON data
        if json_data is None or json_data == {}:
            return jsonify({"message": "ERROR: Request data not found"}), 400

        # Ensures that the song ID is an integer
        try:
            # Retrieves the ID from the request body. If absent, returns None.
            # Then attempts to convert the ID to an integer.
            # Raises a ValueError if the conversion fails (e.g., "abc").
            # Raises a TypeError if ID is None (as int(None) is not allowed).

            # Use .get() to avoid KeyError if 'id' is missing
            song_id = int(json_data.get('id'))

        except (ValueError, TypeError):   # Cases where ID not valid / missing
            message_str = "ERROR: 'id' shall be a valid integer "
            message_str += "in the request body"
            return jsonify({"message": message_str}), 400

        # Replaces the ID in json_data with its integer version for insertion
        json_data['id'] = song_id

        # Checks if the song with the specified ID already exists
        existing_song = current_app.db.songs.find_one({'id': json_data['id']})

        if existing_song is not None:
            message_str = f"song with id {json_data['id']} already present"
            return jsonify({"message": message_str}), 302

        # Inserts the new song
        result = current_app.db.songs.insert_one(json_data)

        # Returns the inserted ID
        rtrn_message = {"inserted_id": parse_json(result.inserted_id)}
        return jsonify(rtrn_message), 201  # 201 Created

    @app_instance.route('/song/<string:id_str>', methods=["PUT"])
    def update_song(id_str: str) -> Tuple[Response, int]:
        """
        Updates an existing song by its ID.

        Args:
            id_str (str): The ID of the song to update.

        Returns:
            Tuple[Response, int]: A tuple containing a JSON response
            and an HTTP status code.
        """
        try:
            id = int(id_str)
        except ValueError:
            message_str = "ERROR: Invalid ID format. "
            message_str += f"Its actual value is '{id_str}'"
            return jsonify({"message": message_str}), 400

        if id <= 0:
            message_str = "ERROR: ID must be a positive integer. "
            message_str += f"Its actual value is {id}"
            return jsonify({"message": message_str}), 400

        json_data: Dict[str, Any] = request.get_json()

        # Checks the existence of some JSON data
        if json_data is None:
            return jsonify({"message": "ERROR: Request data not found"}), 400

        # Checks if the song with the specified ID already exists
        existing_song = current_app.db.songs.find_one({'id': id})
        if (existing_song is None):
            return jsonify({"message": "Song not found"}), 404

        # Updates the song
        result = current_app.db.songs.update_one(
                    {'id': id},
                    {'$set': {key: json_data[key] for key in json_data.keys()}}
                )

        status_code: int = 200
        if result.modified_count == 0:
            response_message = {"message": "Song found, but nothing updated"}

        else:
            # Retrieves the updated song
            updated_song = current_app.db.songs.find_one({'id': id})

            # Compares the whole data before and after the update
            response_message = {
                key: updated_song[key]
                for key in json_data.keys()
                if updated_song[key] != existing_song.get(key)
            }

            # Displays the updated attributes
            response_message['_id'] = parse_json(updated_song['_id'])
            response_message['id'] = id
            status_code = 201

        return jsonify(response_message), status_code

    @app_instance.route('/song/<string:id_str>', methods=["DELETE"])
    def delete_song(id_str: str) -> Tuple[Response, int]:
        """
        Deletes a song by its ID.

        Args:
            id_str (str): The ID of the song to delete.

        Returns:
            Tuple[Response, int]: A tuple containing a JSON response
            and an HTTP status code.
        """
        try:
            id = int(id_str)
        except ValueError:
            message_str = "ERROR: Invalid ID format. "
            message_str += f"Its actual value is '{id_str}'"
            return jsonify({"message": message_str}), 400

        if id <= 0:
            message_str = "ERROR: ID must be a positive integer. "
            message_str += f"Its value is {id}"
            return jsonify({"message": message_str}), 400

        # Deletes entity whise ID is id
        result = current_app.db.songs.delete_one({'id': id})

        if result.deleted_count == 0:
            return jsonify({"message": "Song not found"}), 404
        elif result.deleted_count == 1:
            return "", 204
        else:
            return jsonify({"message": "ERROR: Unexpected error"}), 500
