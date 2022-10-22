#!/usr/bin/python3
"""
Create an app instance
"""
import os
from flask import Flask

from . import models
from .views import app_views

app = Flask(__name__)

app.register_blueprint(app_views)


@app.teardown_appcontext
def close_db(e=None):
    """
    Registers a function to be called after each request and app processs
    """
    models.storage.close()


@app.errorhandler(404)
def not_found(e=None):
    """
    Handling not found JSON response
    """
    return {"error": "Not found"}, 404


if __name__ == "__main__":
    host = os.getenv("HBNB_API_HOST", "0.0.0.0")
    port = os.getenv("HBNB_API_PORT", 5000)
    app.run(host=host, port=port, threaded=True)
