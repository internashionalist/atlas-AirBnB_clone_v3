#!/usr/bin/python3
"""
This module creates a new view for Place Review objects
to handle all default RestFul API actions.
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route("/places/<place_id>/reviews", methods=["GET"],
                 strict_slashes=False)
def get_all_reviews(place_id):
    """
    retrieves list of all Review objects of a Place
    """
    place = storage.get(Place, place_id)
    """using get method to fetch a place with
    a specified place_id"""
    if place:
        reviews_json = []
        for review in place.reviews:
            reviews_json.append(review.to_dict())
            """If the place object exists,
            initialize an empty list called reviews_json to store
            Review objects in JSON format"""
        return jsonify(reviews_json)
        """the reviews_json list is returned as a JSON
        resonse using jsonify."""
    else:
        abort(404)
        """If the place object was not found, abort the
        request with a 404 error message."""


@app_views.route("/reviews/<review_id>", methods=["GET"],
                 strict_slashes=False)
def get_review_id(review_id):
    """
    retrieves a Review object by id
    """
    review = storage.get(Review, review_id)
    """using a get method to fetch a review by its
    review_id."""
    if review:
        return jsonify(review.to_dict())
        """If the review object exists, to_dict() converts
        it into a dictionary and returned as a json response
        using jsonify"""
    else:
        abort(404)
        """if the review object doesn't exist
        abort request with a 404 error message"""


@app_views.route("/reviews/<review_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_review(review_id):
    """
    deletes a Review object by id
    """
    review = storage.get(Review, review_id)
    """fetches a review by its review_id using a get method"""
    if review:
        storage.delete(review)
        storage.save()
        return jsonify({}), 200
        """if the review object exists, it is deleted.
        save() saves the deletion in storage.
        jsonify({}) returns an empty JSON response with a 
        200 status message indicating successful deletion
        """
    else:
        abort(404)
        """If the review object doesn't exist
        abort the request with a 404 error message"""


@app_views.route("/places/<place_id>/reviews", methods=["POST"],
                 strict_slashes=False)
def post_review(place_id):
    """
    creates a Review object
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
        """uses get method to fetch a Place object with
        a specified place_id. If its not found, abort request with
        404 error message"""

    if not request.is_json:
        abort(400, "Not a JSON")
        """is_json checks if the request contains JSON data.
        Aborts request if no JSON data"""

    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
        """get_json retrieves the JSON data.
        if there is no data, abort request"""

    if "user_id" not in data:
        abort(400, "Missing user_id")

    if "text" not in data:
        abort(400, "Missing text")
        """if user_id or text is missing from JSON data,
        abort request with a 400 error message"""

    user = storage.get(User, data["user_id"])
    if not user:
        abort(404)
        """retrieves the User object associated with the provided user_id
        from the JSON data using get method.
        If user doesn't exist, abort request."""

    new_review = Review(**data)
    new_review.place_id = place_id
    new_review.save()
    return jsonify(new_review.to_dict()), 201
    """New review object is created using the data provided.
    place_id is set for the Review object.
    The new review is saved and the details of the new review
    are converted to a dictionary using to_dict() and
    returned as a JSON response with jsonify. a 201 status
    code will appear to indicate a successful creation"""


@app_views.route("/reviews/<review_id>", methods=["PUT"],
                 strict_slashes=False)
def put_review(review_id):
    """
    updates a Review object by id
    """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
        """uses get method to fetch a review object with
        a specified review_id. If the review doesn't exist,
        abort with 404 error message."""

    if not request.is_json:
        abort(400, "Not a JSON")
        """is_json checks if the request contains JSON data.
        If not, abort with 400 error code message"""

    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
        """get_json() retrieves the JSON data.
        If the data is none, abort request with 400 error
        message"""

    excluded_keys = ["id", "user_id", "place_id", "created_at", "updated_at"]
    for key, value in data.items():
        if key not in excluded_keys:
            setattr(review, key, value)
            """excluded_keys are protected from ever being updated.
            Iterates through key-values in data dictionary, and if the
            key is not an excluded_key, setattr updates the review object"""

    review.save()
    return jsonify(review.to_dict()), 200
    """The new review object is saved, and is returned as a JSON response.
    A 200 status code will appear, indicating a successful update"""
