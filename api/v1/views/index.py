#!/usr/bin/python3
"""
This module contains the status and stats routes.
"""
from flask import jsonify
from api.v1.views import app_views


@app_views.route("/status")
def status():
    """ returns the status of the API """
    return jsonify({"status": "OK"})


@app_views.route("/stats")
def stats():
    """ returns the STATS of the API """
    from models import storage

    classes = {
        "amenities": "Amenity",
        "cities": "City",
        "places": "Place",
        "reviews": "Review",
        "states": "State",
        "users": "User",
    }

    stats_dict = {}
    for key, value in classes.items():
        stats_dict[key] = storage.count(value)
    return jsonify(stats_dict)
