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
    return jsonify(states_json)


@app_views.route("/states/<state_id>", methods=["GET"],
                 strict_slashes=False)
def get_state_id(state_id):
    """
    retrieves a State object by id
    """
    state = storage.get(State, state_id)
    if state:
        return jsonify(state.to_dict())
    else:
        abort(404)


@app_views.route("/states/<state_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_state(state_id):
    """
    deletes a State object
    """
    state = storage.get(State, state_id)
    if state:
        storage.delete(state)
        storage.save()
        return jsonify({})
    else:
        abort(404)


@app_views.route("/states", methods=["POST"],
                 strict_slashes=False)
def post_state():
    """
    creates a State object
    """
    if not request.is_json():
        abort(400, "Not a JSON")

    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    if "name" not in data:
        abort(400, "Missing name")
    new_state = State(**data)
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route("/states/<state_id>", methods=["PUT"],
                 strict_slashes=False)
def put_state(state_id):
    """
    updates a State object
    """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")
    for key, value in request.get_json().items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict())
