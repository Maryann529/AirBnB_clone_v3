#!/usr/bin/python3
"""
A new view for Amenity objects that handles all default RESTFul API actions
"""
from flask import abort
from flask import jsonify
from flask import request

from . import Amenity
from . import storage
from . import app_views

# f are class properties to validate the request payload
f = ("name",)


@app_views.route("/amenities", methods=["GET", "POST"], strict_slashes=False)
def all_amenities():
    """
    Creates a new Amenity obj
    Retrieves the list of all City objects of a Amenity
    Args:
        state_id: primary key of an existing Amenity object
    """
    if request.method == "GET":
        return jsonify([a.to_dict() for a in storage.all(Amenity).values()])
    else:
        body = request.get_json(silent=True)
        if request.is_json and body:
            pay = {k: v for k, v in body.items() if k in f}
            if not pay.get("name", None):
                return jsonify({"message": "Missing name"}), 400
            new_amenity = Amenity(**pay)
            storage.new(new_amenity), storage.save()
            return jsonify(new_amenity.to_dict()), 201
        return jsonify({"message": "Not a JSON"}), 400


@app_views.route("/amenities/<amenity_id>",
                 methods=["GET", "PUT", "DELETE"], strict_slashes=False)
def one_amenity(amenity_id):
    """
    Deletes an existing Amenity object
    Retrieves an existing Amenity object
    Updates an existing Amenity object
    Args:
        city_id: primary key of an existing Amenity object
    """
    amen = storage.get(Amenity, amenity_id)
    if not amen:
        abort(404)
    if request.method == "GET":
        return amen.to_dict()
    elif request.method == "DELETE":
        storage.delete(amen), storage.save()
        return {}
    else:
        body = request.get_json(silent=True)
        if request.is_json and body:
            [amen.__dict__.update({k: v}) for k, v in body.items() if k in f]
            amen.save()
            return jsonify(amen.to_dict()), 200
        return jsonify({"message": "Not a JSON"}), 400
