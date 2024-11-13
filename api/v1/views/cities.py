#!/usr/bin/python3
"""
This module creates a new view for City objects
to handle all default RestFul API actions.
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State
from models.city import City


@app_views.route("/states/<state_id>/cities", methods=["GET"],
                 strict_slashes=False)
def get_all_cities(state_id):
    """
    retrieves list of all City objects
    """
    state = storage.get(State, state_id)
    """fetches a State object from storage using get method
    with a specified state_id"""
    if state:
        cities_json = [city.to_dict() for city in state.cities]
        return jsonify(cities_json)
        """if the State object exists, iterates through each
        city in state.cities and converts each city object into
        a dictionary using to_dict() method. The resulting list
        of dictionaries is assigned to a list called cities_json
        Then, cities_json is returned as a JSON response with
        jsonify"""
    else:
        abort(404)
        """if the state isn't found, abort the request and display
        a 404 error message"""


@app_views.route("/cities/<city_id>", methods=["GET"],
                 strict_slashes=False)
def get_city_id(city_id):
    """
    retrieves a City object by id
    """
    city = storage.get(City, city_id)
    """fetches a city from storage with a specific
    city_id using get method"""
    if city:
        return jsonify(city.to_dict())
        """If the city exists, to_dict() converts the
        City object to a dictionary and is returned
        as a JSON response using jsonify"""
    else:
        abort(404)
        """If state object isn't found, abort request with
        a 404 error message"""


@app_views.route("/cities/<city_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_city(city_id):
    """
    deletes a City object
    """
    city = storage.get(City, city_id)
    """fetch city object witha specific city_id
    using get method"""
    if city:
        storage.delete(city)
        storage.save()
        return jsonify({})
        """if the city object exists, delete the City from stoage.
        save() saves the deletion in storage.
        jsonify({}) returns an empty JSON response"""
    else:
        abort(404)
        """if the city object isn't found, abort request
        with 404 error message"""


@app_views.route("/states/<state_id>/cities", methods=["POST"],
                 strict_slashes=False)
def post_city(state_id):
    """
    creates a City object
    """
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    if not request.is_json:
        abort(400, "Not a JSON")

    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")

    if "name" not in data:
        abort(400, "Missing name")

    city = City(**data)
    city.state_id = state_id
    city.save()
    return jsonify(city.to_dict()), 201


@app_views.route("/cities/<city_id>", methods=["PUT"],
                 strict_slashes=False)
def put_city(city_id):
    """
    updates a City object
    """
    city = storage.get(City, city_id)
    """fetches a City object with a specified city_id
    using a get method"""
    if not city:
        abort(404)
        """If the city isn't found, abort request"""

    if not request.is_json:
        abort(400, "Not a JSON")
        """is_json checks if the object contains
        JSON data"""

    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
        """get_json() retrieves all of the JSON data.
        If there is no JSON data, abort request."""

    for key, value in data.items():
        if key not in ["id", "state_id", "created_at", "updated_at"]:
            setattr(city, key, value)
            """Iterates through all key-values and updates the keys that
            aren't id, state_id, created_at, updated_at."""

    city.save()
    return jsonify(city.to_dict())
    """save() saves the updated changes to the city object.
    the object is then converted into a dictionary and returned
    as a JSON response"""
