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
    if city:
        places_json = []
        for place in city.places:
            places_json.append(place.to_dict())
        return jsonify(places_json)
    else:
        abort(404)


@app_views.route("/places/<place_id>", methods=["GET"],
                 strict_slashes=False)
def get_place_id(place_id):
    """
    retrieves a Place object by id
    """
    place = storage.get(Place, place_id)
    if place:
        return jsonify(place.to_dict())
    else:
        abort(404)


@app_views.route("/places/<place_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_place(place_id):
    """
    deletes a Place object by id
    """
    place = storage.get(Place, place_id)
    if place:
        storage.delete(place)
        storage.save()
        return jsonify({})
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
    if not request.get_json():
        abort(400, "Not a JSON")
    if "user_id" not in request.get_json():
        abort(400, "Missing user_id")
    if not storage.get(User, request.get_json()["user_id"]):
        abort(404)
    if "name" not in request.get_json():
        abort(400, "Missing name")
    place = Place(**request.get_json())
    place.city_id = city_id
    place.save()
    return jsonify(place.to_dict())


@app_views.route("/places/<place_id>", methods=["PUT"],
                 strict_slashes=False)
def put_place(place_id):
    """
    updates a Place object
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")
    for key, value in request.get_json().items():
        if key not in ["id", "user_id", "city_id", "created_at", "updated_at"]:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict())


@app_views.route("/places_search", methods=["POST"],
                 strict_slashes=False)
def post_places_search():
    """
    retrieves a list of Place objects based on JSON search
    """
    if not request.get_json():
        abort(400, "Not a JSON")
    places = storage.all(Place).values()
    places_json = []
    if "states" in request.get_json():
        for state_id in request.get_json()["states"]:
            state = storage.get(State, state_id)
            if state:
                for city in state.cities:
                    for place in city.places:
                        places_json.append(place.to_dict())
    if "cities" in request.get_json():
        for city_id in request.get_json()["cities"]:
            city = storage.get(City, city_id)
            if city:
                for place in city.places:
                    places_json.append(place.to_dict())
    if "amenities" in request.get_json():
        for amenity_id in request.get_json()["amenities"]:
            amenity = storage.get(Amenity, amenity_id)
            if amenity:
                for place in amenity.places:
                    places_json.append(place.to_dict())
    return jsonify(places_json)
