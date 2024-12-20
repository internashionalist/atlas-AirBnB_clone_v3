#!/usr/bin/python3
"""
This module starts a Flask web application.
"""
from api.v1.views import app_views
from flask import Flask, jsonify, make_response
from flask_cors import CORS
from models import storage
import os


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown_db(exception):
    """
    closes the storage session after each request
    """
    storage.close()


@app.errorhandler(404)
def not_found_404(error):
    """
    returns a JSON-formatted 404 status code response
    """
    return (jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    host = os.getenv("HBNB_API_HOST", "0.0.0.0")
    port = int(os.getenv("HBNB_API_PORT", 5000))
    app.run(host=host, port=port, threaded=True)
