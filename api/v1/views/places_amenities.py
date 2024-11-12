#!/usr/bin/python3
"""
This module defines API actions for linking Place and Amenity objects.
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.amenity import Amenity
from os import getenv

storage_t = getenv("HBNB_TYPE_STORAGE")


@app_views.route("/places/<place_id>/amenities", methods=["GET"],
                 strict_slashes=False)
def place_amenities_get(place_id):
    """
    retrieves list of all Amenity objects of a Place
    """
    place = storage.get(Place, place_id)
    if place:
        if storage_t == "db":
            amenities = place.amenities
        else:
            for amenity_id in place.amenity_ids:
                amenities.append(storage.get(Amenity, amenity_id))

        amenities_json = []
        for amenity in amenities:
            amenities_json.append(amenity.to_dict())
        return jsonify(amenities_json)
    else:
        abort(404)


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 methods=["DELETE"], strict_slashes=False)
def place_amenity_delete(place_id, amenity_id):
    """
    deletes an Amenity object from a Place
    """
    place = storage.get(Place, place_id)
    if place:
        amenity = storage.get(Amenity, amenity_id)
        if amenity:
            if storage_t == "db":
                if amenity in place.amenities:
                    place.amenities.remove(amenity)
                else:
                    abort(404)
            else:
                if amenity_id in place.amenity_ids:
                    place.amenity_ids.remove(amenity_id)
                else:
                    abort(404)
        else:
            abort(404)
    else:
        abort(404)


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 methods=["POST"], strict_slashes=False)
def place_amenity_link(place_id, amenity_id):
    """
    links an Amenity object to a Place
    """
    place = storage.get(Place, place_id)
    if place:
        amenity = storage.get(Amenity, amenity_id)
        if amenity:
            if storage_t == "db":
                if amenity in place.amenities:
                    return jsonify(amenity.to_dict()), 200
                place.amenities.append(amenity)
            else:
                if amenity_id in place.amenity_ids:
                    return jsonify(amenity.to_dict()), 200
                place.amenity_ids.append(amenity_id)
            storage.save()
            return jsonify(amenity.to_dict()), 201
        else:
            abort(404)
    else:
        abort(404)
