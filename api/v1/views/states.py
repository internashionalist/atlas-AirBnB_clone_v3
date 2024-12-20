#!/usr/bin/python3
"""
This module creates a new view for State objects
to handle all default RestFul API actions.
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State


@app_views.route("/states", methods=["GET"],
                 strict_slashes=False)
def get_all_states():
    """
    retrieves list of all State objects
    """
    states_json = [state.to_dict() for state in storage.all(State).values()]
    """creates a list of dictionaries called states_json.
    Iterates through all State objects in storage.all(State.values(),
    to_dict converts each State into a dictionary and adds it
    to states_json list.)"""
    return jsonify(states_json)
    """jsonify turns the states_json list into a JSON response"""


@app_views.route("/states/<state_id>", methods=["GET"],
                 strict_slashes=False)
def get_state_id(state_id):
    """
    retrieves a State object by id
    """
    state = storage.get(State, state_id)
    """Using get method to fetch a State object with a
    specified state_id"""
    if state:
        return jsonify(state.to_dict())
        """If the state exists, its converted into a dictionary
        using to_dict(), then returned as a JSON response using
        jsonify."""
    else:
        abort(404)
        """if the state doesn't exist, the request is aborted
        with a 404 error message appearing"""


@app_views.route("/states/<state_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_state(state_id):
    """
    deletes a State object
    """
    state = storage.get(State, state_id)
    """get method to fetch a State with a specified state_id
    from the storage object."""
    if state:
        storage.delete(state)
        storage.save()
        return jsonify({})
        """If the State exists, the State is deleted and saved to storage.
        Then, an empty json response is returned with jsonify({})"""
    else:
        abort(404)
        """If the State doesn't exist, the request is aborted."""


@app_views.route("/states", methods=["POST"],
                 strict_slashes=False)
def post_state():
    """
    creates a State object
    """
    if not request.is_json:
        abort(400, "Not a JSON")
        """Checks if the request contains JSON data.
        If not, request is aborted with 400 error message"""

    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    if "name" not in data:
        abort(400, "Missing name")
        """get_json retrieves all of the json data.
        If the data is none or is missing a State Name,
        request is aborted with a 400 error message."""

    new_state = State(**data)
    new_state.save()
    return jsonify(new_state.to_dict()), 201
    """A new_state object is created using the data provided.
    save() saves new_state. Then its converted to a dictionary
    and returned as a JSON response with return jsonfiy.
    A 201 message is appear, indicating a successfull creation."""


@app_views.route("/states/<state_id>", methods=["PUT"],
                 strict_slashes=False)
def put_state(state_id):
    """
    updates a State object
    """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
        """Using a get method to fetch a State object
        with a specified state_id from Storage.
        If State doesn't exist, request aborted."""

    if not request.is_json:
        abort(400, "Not a JSON")
        """is_json checks if the request contains JSON data.
        If no JSON data, abort request with error message."""

    data = request.get_json()
    for key, value in data.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(state, key, value)
            """Iterates through the data dictionary and updates
            the State object with values excluding id,
            created_at, updated_at."""

    state.save()
    return jsonify(state.to_dict())
    """save() saves the updated State.
    Then the updated details are returned in JSON format."""
