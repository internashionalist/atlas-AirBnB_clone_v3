#!/usr/bin/python3
"""
This module creates a new view for Place objects
to handle all default RestFul API actions.
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.state import State
from models.user import User


@app_views.route("/cities/<city_id>/places", methods=["GET"],
                 strict_slashes=False)
def get_all_places(city_id):
    """
    retrieves list of all Place objects of a City
    """
    city = storage.get(City, city_id)
    """Fetches City from storage with a
    specified city_id"""
    if city:
        places_json = []
        """if City exists, initialize an empty list
        called places_json to store places objects in
        JSON format."""
        for place in city.places:
            places_json.append(place.to_dict())
            """iterates through all Place objects that are
            associated with City, the converts them into
            dictionaries and appends it to the places_json
            list."""
        return jsonify(places_json)
        """The places_json list is returned as a JSON response"""
    else:
        abort(404)
        """If the city was not found, abort the request
        with a 404 error message."""


@app_views.route("/places/<place_id>", methods=["GET"],
                 strict_slashes=False)
def get_place_id(place_id):
    """
    retrieves a Place object by id
    """
    place = storage.get(Place, place_id)
    """using a get method, fetches a Place object with a
    specified place_id."""
    if place:
        return jsonify(place.to_dict())
        """If the place object exists, it is converted
        into a dictionary using to_dict(), then returned
        as a JSON response with jsonify."""
    else:
        abort(404)
        """If place doesn't exist, abort request with 404
        error message."""


@app_views.route("/places/<place_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_place(place_id):
    """
    deletes a Place object by id
    """
    place = storage.get(Place, place_id)
    """fetch Place using get method with a specified
    place_id."""
    if place:
        storage.delete(place)
        storage.save()
        return jsonify({})
        """if Place exists, delete method delets the place.
        Then, the deletion is saved in Storage.
        jsonify{} returns an empty JSON response"""
    else:
        abort(404)


@app_views.route("/cities/<city_id>/places", methods=["POST"],
                 strict_slashes=False)
def post_place(city_id):
    """
    creates a Place object
    """
    city = storage.get(City, city_id)
    """Using get method to fetch a City with a
    specified city_id"""
    if not city:
        abort(404)
        """Abort request with 404 error message if
        city doesn't exist."""

    if not request.is_json:
        abort(400, "Not a JSON")
        """is_json checks if the request contains
        JSON data. """

    data = request.get_json()
    if "user_id" not in data:
        abort(400, "Missing user_id")

    if not storage.get(User, data["user_id"]):
        abort(404)

    if "name" not in data:
        abort(400, "Missing name")
        """get_json retrieves the JSON data.
        Then, it checks for user_id and name.
        If user_id is missing, 400 error. Another
        check if the User associated with the user_id
        exists."""

    place = Place(**data)
    place.city_id = city_id
    place.save()
    return jsonify(place.to_dict()), 201
    """Place(**data) creates a new Place object using the data provided.
    The city_id is set for the Place object. save() saves the new Place.
    the new details are returned as JSON response, and a 201 message
    appears to indicate successful creation."""


@app_views.route("/places/<place_id>", methods=["PUT"],
                 strict_slashes=False)
def put_place(place_id):
    """
    updates a Place object
    """
    place = storage.get(Place, place_id)
    """Fetches a place with a get method using a specified
    place_id"""
    if not place:
        abort(404)
        """If Place doesn't exist, abort request
        with a 404 error message."""

    if not request.is_json:
        abort(400, "Not a JSON")
        """is_json checks if the request
        contains JSON data. If not, abort rquest
        with a 400 error message."""

    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
        """get_json() retrieves the JSON data.
        if there is no data, abort request with
        an error message"""
    excluded_keys = ["id", "user_id", "city_id", "created_at", "updated_at"]
    """excluded_keys will be keys that we want to ignore later/ protect
    the values from being updated."""
    for key, value in data.items():
        if key not in excluded_keys:
            setattr(place, key, value)
            """iterates through the key-values in the data dictionary.
            If the key is not in excluded_keys, it is updated using
            setattr()"""

    place.save()
    return jsonify(place.to_dict())
    """save() saves the updated place.
    the new place object is converted into a dictionary using to_dict()
    the, returned as a JSON response using jsonify"""


@app_views.route("/places_search", methods=["POST"],
                 strict_slashes=False)
def post_places_search():
    """
    retrieves a list of Place objects based on JSON search
    """
    if not request.is_json:
        abort(400, "Not a JSON")

    data = request.get_json()

    places_json = []
    if "states" in data:
        for state_id in data["states"]:
            state = storage.get(State, state_id)
            if state:
                for city in state.cities:
                    for place in city.places:
                        places_json.append(place.to_dict())

    if "cities" in data:
        for city_id in data["cities"]:
            city = storage.get(City, city_id)
            if city:
                for place in city.places:
                    places_json.append(place.to_dict())

    if "amenities" in data:
        for amenity_id in data["amenities"]:
            amenity = storage.get(Amenity, amenity_id)
            if amenity:
                for place in amenity.places:
                    places_json.append(place.to_dict())

    return jsonify(places_json)
