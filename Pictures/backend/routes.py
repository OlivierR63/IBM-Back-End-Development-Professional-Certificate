from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    """Retrieve all pictures.

    Returns:
        Response: A Flask response object containing the list of pictures
        in JSON format if available, or an empty list with a 200 status code
        if no pictures are found.
    """
    if data:
        return jsonify(data), 200
    else:
        return jsonify([]), 200


######################################################################
# GET A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    """Retrieve a picture by its ID.

    Args:
        id (int): The ID of the picture to retrieve.

    Returns:
        Response: A Flask response object containing the picture data
        in JSON format if found, or an error message if the picture
        is not found.
    """
    if data:
        for picture in data:
            try:
                if int(picture["id"]) == id:
                    return jsonify(picture), 200
            except (KeyError, ValueError):
                # Handle the case where 'id' key is missing or cannot
                # be converted to an integer
                continue

    return jsonify({"message": f"Picture with id {id} not found"}), 404


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    """Create a new picture and add it to the data list.

    Expects:
        JSON data representing the new picture.

    Returns:
        Response: A Flask response object containing a success message
        and the new picture data, or an error message if the request
        is invalid.
    """
    # Check if the request contains JSON data
    if not request.is_json:
        return jsonify({"Message": "Missing JSON in request"}), 400

    # Extract JSON data from the request
    new_picture = request.get_json()

    # Validate the data (you can add additional validations here)
    if not new_picture:
        return jsonify({"Message": "Invalid picture data"}), 400

    for picture in data:
        if new_picture['id'] == picture['id']:
            msg_str = f"picture with id {picture['id']} already present"
            return jsonify({"Message": msg_str,
                            "picture": new_picture,
                            'id': new_picture['id']}), 302

    # Add the new picture to the data list
    data.append(new_picture)

    # Return a success response with the new picture data
    msg_str = "Picture added successfully"
    return jsonify({
                        "Message": msg_str,
                        "picture": new_picture,
                        'id': new_picture['id']
                    }), 201


######################################################################
# UPDATE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    """
    Update a picture in the data list based on the provided ID.

    This function handles PUT requests to update the details of a
    specific picture. It checks if the request contains valid JSON data,
    searches for the picture by ID, and updates its details if found.
    If the picture is not found, it returns a 404 error.

    Parameters:
    - id (int): The ID of the picture to update.

    Returns:
    - Response: A Flask response object with a JSON body and appropriate
                HTTP status code, whose return status code is:
                200 if the picture is successfully deleted.
                400 if the ID is invalid.
                404 if the picture with the specified ID is not found.
    """

    # Check if the request contains JSON data
    if not request.is_json:
        return jsonify({"Message": "Missing JSON in request"}), 400

    # Extract JSON data from the request
    request_picture = request.get_json()

    # Validate the request data
    if not request_picture or 'id' not in request_picture:
        return jsonify({"Message": "Invalid data in request"}), 400

    for picture in data:
        if id == picture['id']:
            for key in request_picture.keys():
                picture[key] = request_picture[key]

            msg_str = "Picture updated successfully"
            return jsonify({
                                "Message": msg_str,
                                "picture": picture,
                                'id': id
                            }), 200
    else:
        msg_str = f"Picture whose id is {id} not found"
        return jsonify({
                            "Message": msg_str,
                            "picture": request_picture,
                            'id': id
                        }), 404


######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id: int):
    """
    Delete a picture from the data list based on the provided ID.
    This function handles DELETE requests to remove a specific picture by
    its ID. It checks if the ID is valid, searches for the picture by ID,
    and removes it if found. If the picture is not found, it returns
    a 404 error.

    Parameters:
    - id (int): The ID of the picture to delete.

    Returns:
    - Response: A Flask response object with a JSON body and appropriate
                HTTP status code, whose return status code is:
                200 if the picture is successfully deleted.
                400 if the ID is invalid.
                404 if the picture with the specified ID is not found.
    """
    # Validate the request data
    if not isinstance(id, int) or id < 0:
        return jsonify({"Message": "Invalid data in request"}), 400

    for picture in data:
        if picture['id'] == id:
            data.remove(picture)
            message_str = f"Picture whose id is {id} removed"
            return jsonify({"Message": message_str}), 204

    return jsonify({"Message": f"Picture whose id is {id} not found"}), 404
