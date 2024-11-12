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
    if user:
        storage.delete(user)
        storage.save()
        return jsonify({})
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

    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")

    if "email" not in data:
        abort(400, "Missing email")

    if "password" not in data:
        abort(400, "Missing password")

    user = User(**data)
    user.save()
    return jsonify(user.to_dict()), 201


@app_views.route("/users/<user_id>", methods=["PUT"],
                 strict_slashes=False)
def put_user(user_id):
    """
    updates a User object by id
    """
    user = storage.get(User, user_id)
    if not user:
        abort(404)

    if not request.is_json:
        abort(400, "Not a JSON")

    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")

    for key, value in data.items():
        if key not in ["id", "email", "created_at", "updated_at"]:
            setattr(user, key, value)

    user.save()
    return jsonify(user.to_dict())
