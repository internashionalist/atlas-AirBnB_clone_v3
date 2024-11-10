#!/usr/bin/python3
"""
This module creates a new view for Amenity objects
to handle all default RestFul API actions.
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity


@app_views.route("/amenities", methods=["GET"],
                 strict_slashes=False)
def get_all_amenities():
    """
    retrieves list of all Amenity objects
    """
    amenities = []
    for amenity in storage.all(Amenity).values():
        amenities.append(amenity.to_dict())
    return jsonify(amenities)


@app_views.route("/amenities/<amenity_id>", methods=["GET"],
                 strict_slashes=False)
def get_amenity_id(amenity_id):
    """
    retrieves an Amenity object by id
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        return jsonify(amenity.to_dict())
    else:
        abort(404)


@app_views.route("/amenities/<amenity_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """
    deletes an Amenity object
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        storage.delete(amenity)
        storage.save()
        return jsonify({})
    else:
        abort(404)


@app_views.route("/amenities", methods=["POST"],
                 strict_slashes=False)
def post_amenity():
    """
    creates an Amenity object
    """
    if not request.is_json:
        abort(400, "Not a JSON")

    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")

    if "name" not in data:
        abort(400, "Missing name")

    amenity = Amenity(**data)
    amenity.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route("/amenities/<amenity_id>", methods=["PUT"],
                 strict_slashes=False)
def put_amenity(amenity_id):
    """
    updates an Amenity object
    """
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    if not request.is_json:
        abort(400, "Not a JSON")

    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")

    for key, value in data.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(amenity, key, value)

    amenity.save()
    return jsonify(amenity.to_dict()), 200
