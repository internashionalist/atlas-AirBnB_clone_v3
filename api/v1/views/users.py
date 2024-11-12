#!/usr/bin/python3
"""
This module creates a new view for User objects
to handle all default RestFul API actions.
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.user import User


@app_views.route("/users", methods=["GET"],
                 strict_slashes=False)
def get_all_users():
    """
    retrieves list of all User objects
    """
    users_json = []
    """initializing an empty list called users_json to store the dictionary
    representation of each User object"""
    for user in storage.all(User).values():
        users_json.append(user.to_dict())
    """Iterates through each User object and to_dict()
    gives the dictionary representation and is added to the users_json list"""
    return jsonify(users_json)
    """Jsonify converts the users_json list into a JSON response"""


@app_views.route("/users/<user_id>", methods=["GET"],
                 strict_slashes=False)
def get_user_id(user_id):
    """
    retrieves a User object by id
    """
    user = storage.get(User, user_id)
    """Using a get method to fetch a User from the Storage object with
    a specified user_id """
    if user:
        return jsonify(user.to_dict())
        """if the user is found, it is converted to a dictionary using
        to_dict(), then converted to JSON with jsonify"""
    else:
        abort(404)
        """if the user doesn't exist, a 404 error message will appear"""


@app_views.route("/users/<user_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_user(user_id):
    """
    deletes a User object
    """
    user = storage.get(User, user_id)
    """get method to fetch a User with a specified user_id from the storage object."""
    if user:
        storage.delete(user)
        storage.save()
        return jsonify({})
    """if user exists, the delete method is used to delete the user,
    then the save method saves the changes to storage. Then an empty
    JSON respsone is returned {}"""
    else:
        abort(404)


@app_views.route("/users", methods=["POST"],
                 strict_slashes=False)
def post_user():
    """
    creates a User object
    """
    if not request.is_json:
        abort(400, "Not a JSON")
        """is_Json Checks if the request contains JSON data.
        If there is no JSON data, the request is aborted
        and a 400 error code with message"""

    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
        """get_json retrieves JSON data from the request.
        If there is no data, request is aborted and 400
        error messages appears."""

    if "email" not in data:
        abort(400, "Missing email")

    if "password" not in data:
        abort(400, "Missing password")
        """if either 'email' or 'password' is missing from the JSON data,
        the request is aborted and 400 error message will appear."""

    user = User(**data)
    user.save()
    return jsonify(user.to_dict()), 201
    """if all the required data is present, a new User is created
    with User(**data), then the User is saved to storage with save().
    The user object is then converted to a dictionary and returned 
    as a JSON response. A 201 status message will appear to show a
    successfull User creation."""


@app_views.route("/users/<user_id>", methods=["PUT"],
                 strict_slashes=False)
def put_user(user_id):
    """
    updates a User object by id
    """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
        """Using a get method to fetch User with a specified
        user_id from Storage object. If the user does not exist,
        request aborted and 404 message appears."""

    if not request.is_json:
        abort(400, "Not a JSON")
        """is_json checks if the request contains JSON data.
        If no JSON data, request aborted with 400 error message"""

    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
        """get_json retrieves the JSON data. If there is no data,
        request aborted"""

    for key, value in data.items():
        if key not in ["id", "email", "created_at", "updated_at"]:
            setattr(user, key, value)
            """iterates through the data dictionary and updates
            the keys that are not id, email, created_at, updated_at.
            setattr dynamically updates the user object's attributes"""

    user.save()
    return jsonify(user.to_dict())
    """save() saves the updated user object and returns the
    updated details in JSON format with to_dict() and jsonify"""
