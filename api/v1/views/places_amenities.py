#!/usr/bin/python3
"""
A view for the link between Place objects and
Amenity objects that handles all default RESTFul API actions
"""
import os
from flask import abort
from flask import jsonify
from flask import request

from . import Place
from . import Amenity
from . import storage
from . import app_views


@app_views.route("/places/<place_id>/amenities", strict_slashes=False)
def amenities_by_place(place_id):
    """
    Retrieves the list of all Amenity objects of a Place
    """
    place = storage.get(Place, str(place_id))
    if place is None:
        abort(404, description="Not found")
    return jsonify([a.to_dict() for a in place.amenities])


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 methods=["POST", "DELETE"], strict_slashes=False)
def one_amenity_in_place(amenity_id, place_id):
    """
    Deletes a Amenity object to a Place
    Args:
        amenity_id (str): id of an Amenity object
        place_id (str): id of a Place object
    """
    pass
