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
    if not city:
        abort(404)

    if not request.is_json:
        abort(400, "Not a JSON")

    data = request.get_json()
    if "user_id" not in data:
        abort(400, "Missing user_id")

    if not storage.get(User, data["user_id"]):
        abort(404)

    if "name" not in data:
        abort(400, "Missing name")

    place = Place(**data)
    place.city_id = city_id
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.route("/places/<place_id>", methods=["PUT"],
                 strict_slashes=False)
def put_place(place_id):
    """
    updates a Place object
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    if not request.is_json:
        abort(400, "Not a JSON")

    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    excluded_keys = ["id", "user_id", "city_id", "created_at", "updated_at"]
    for key, value in data.items():
        if key not in excluded_keys:
            setattr(place, key, value)

    place.save()
    return jsonify(place.to_dict())


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
