#!/usr/bin/python3
"""
This module contains the status and stats routes.
"""
from flask import jsonify
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route("/status")
def status():
    """ returns the status of the API """
    return jsonify({"status": "OK"})


@app_views.route("/stats")
def stats():
    """ returns the STATS of the API """
    classes = {
        "amenities": Amenity,
        "cities": City,
        "places": Place,
        "reviews": Review,
        "states": State,
        "users": User,
    }

    stats_dict = {}
    for key, cls in classes.items():
        stats_dict[key] = storage.count(cls)
    return jsonify(stats_dict)
