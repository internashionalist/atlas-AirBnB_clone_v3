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
    """Initializes an empty list to store Amenity objects in
    JSON format"""
    for amenity in storage.all(Amenity).values():
        amenities.append(amenity.to_dict())
        """iterates through all Amenity objects returned by
        storage.all(Amenity).values(). Each Amenity object is
        converted to a dictionary with to_dict(), and then is
        appended to the amenities list"""
    return jsonify(amenities)
    """returning the amenities list as a JSON response
    using jsonify()"""


@app_views.route("/amenities/<amenity_id>", methods=["GET"],
                 strict_slashes=False)
def get_amenity_id(amenity_id):
    """
    retrieves an Amenity object by id
    """
    amenity = storage.get(Amenity, amenity_id)
    """fetches Amenity object from storage with a specified
    amenity_id"""
    if amenity:
        return jsonify(amenity.to_dict())
        """If the amenity is found, it is converted to a dictionary
        and returned as a JSON response"""
    else:
        abort(404)
        """If the amenity isn't found, abort request with a 404
        error message"""


@app_views.route("/amenities/<amenity_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """
    deletes an Amenity object
    """
    amenity = storage.get(Amenity, amenity_id)
    """fetches an amenity with a specified amenity_id"""
    if amenity:
        storage.delete(amenity)
        storage.save()
        return jsonify({})
        """if the amenity is found, it is deleted from storage,
        the deletion is saved in storage, and then is returned
        as an empty json response"""
    else:
        abort(404)
        """If the amenity isn't found, abort request with a 404
        error message"""


@app_views.route("/amenities", methods=["POST"],
                 strict_slashes=False)
def post_amenity():
    """
    creates an Amenity object
    """
    if not request.is_json:
        abort(400, "Not a JSON")
        """checks if the amenity object contains JSON data.
        If it doesn't, abort the request with a 400 error code"""

    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
        """get_json retrieves the JSON data.
        if the data is none, abort the request"""

    if "name" not in data:
        abort(400, "Missing name")
        """if name isn't included in the JSON data,
        abort the request"""

    amenity = Amenity(**data)
    amenity.save()
    return jsonify(amenity.to_dict()), 201
    """A new amenity object created using the provided data,
    the new Amenity object is saved to storage. The object is
    then converted to a dictionary and returned as a JSON
    response. A 201 status code message will be displayed
    to indicate a successful creation"""


@app_views.route("/amenities/<amenity_id>", methods=["PUT"],
                 strict_slashes=False)
def put_amenity(amenity_id):
    """
    updates an Amenity object
    """
    amenity = storage.get(Amenity, amenity_id)
    """Amenity object is fetched with a specified amenity_id"""
    if not amenity:
        abort(404)
        """If the amenity isn't found, abort the request"""

    if not request.is_json:
        abort(400, "Not a JSON")
        """is_json checks if the object contains JSON data.
        If it doesn't, abort the request."""

    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
        """get_json retrieves all of the json data. If the
        data is none, abort the request"""

    for key, value in data.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(amenity, key, value)
            """iterates through the key-values, and setattr updates keys
            that aren't id, created_at, and updated_at."""

    amenity.save()
    return jsonify(amenity.to_dict()), 200
    """The updated changes are saved with save().
    The updated amenity object is then converted to a dicitonary
    and returned as a JSON response. A 200 status code will appear,
    indicating a successful update"""
