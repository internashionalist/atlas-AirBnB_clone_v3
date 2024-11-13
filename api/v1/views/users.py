#!/usr/bin/python3
"""
This module creates a new view for User objects
to handle all default RestFul API actions.
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.user import User


@app_views.route("/users", methods=["GET"], strict_slashes=False)
def get_all_users():
    """
    retrieves list of all User objects
    """
    users_json = []
    """ initializes empty list to store User objects in JSON format """
    for user in storage.all(User).values():
        users_json.append(user.to_dict())
    """ iterates through all User objects in storage and appends """
    return jsonify(users_json)
    """ returns the list of User objects in JSON format """


@app_views.route("/users/<user_id>", methods=["GET"], strict_slashes=False)
def get_user_id(user_id):
    """
    retrieves a User object by id
    """
    user = storage.get(User, user_id)
    """ uses 'get' to fetch a User with a specified user_id from storage """
    if user:
        return jsonify(user.to_dict())
        """ if user exists, the user object is returned,
            converted to a dictionary as a JSON response """
    else:
        abort(404)
        """ if user doesn't exist, request is aborted with 404 message """


@app_views.route("/users/<user_id>", methods=["DELETE"], strict_slashes=False)
def delete_user(user_id):
    """
    deletes a User object
    """
    user = storage.get(User, user_id)
    """ uses 'get' to fetch a User with a specified user_id from storage """
    if user:
        storage.delete(user)
        storage.save()
        return jsonify({})
        """ if user exists, the user object is deleted from storage,
            storage is saved, and an empty dictionary is returned
            as a JSON response """
    else:
        abort(404)


@app_views.route("/users", methods=["POST"], strict_slashes=False)
def post_user():
    """
    creates a User object
    """
    if not request.is_json:
        abort(400, "Not a JSON")
        """ 'is_json' checks if the request contains JSON data.
            If no JSON data, request is aborted with 400 error message."""

    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
        """ 'get_json' retrieves the JSON data """

    if "email" not in data:
        abort(400, "Missing email")

    if "password" not in data:
        abort(400, "Missing password")
        """ If either 'email' or 'password' is missing from the JSON data,
            the request is aborted and 400 error message will appear. """

    user = User(**data)
    user.save()
    return jsonify(user.to_dict()), 201
    """ If all required data is present, a new User object is created,
        saved, and returned in JSON format with a 201 status code. """


@app_views.route("/users/<user_id>", methods=["PUT"], strict_slashes=False)
def put_user(user_id):
    """
    updates a User object by id
    """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
        """ 'get' fetches a User with a specified user_id from storage. """

    if not request.is_json:
        abort(400, "Not a JSON")
        """ 'is_json' checks if the request contains JSON data.
            if no JSON data, request aborted with 400 error message """

    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
        """ 'get_json' retrieves the JSON data. If there is no data,
            request is aborted with 400 error message. """

    for key, value in data.items():
        if key not in ["id", "email", "created_at", "updated_at"]:
            setattr(user, key, value)
            """ iterates through the JSON data and updates the user object's
                attributes dynamically with 'setattr' """

    user.save()
    return jsonify(user.to_dict())
    """ user object is saved and returned in JSON format """
