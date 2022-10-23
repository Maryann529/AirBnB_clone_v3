#!/usr/bin/python3
"""
A new view for Place objects that handles all default RESTFul API actions
"""
from flask import abort
from flask import jsonify
from flask import request

from . import User
from . import City
from . import Place
from . import storage
from . import app_views

# f are class properties to validate the request payload
f = ("user_id", "name", "description", "number_rooms", "number_bathrooms",
     "max_guest", "price_by_night", "latitude", "longitude")


def validate_payload(payload={}):
    """
    validate type field inputs, ensures the right types are given
    """
    for _ in f[3:7]:
        value = payload.get(_, None)
        if value and value.isnumeric():
            payload.update({_: int(value)})
        else:
            del payload[_]
    for _ in f[-2:]:
        value = payload.get(_, None)
        try:
            if value and isinstance(float(value), float):
                payload.update({_: float(value)})
        except Exception:
            del payload[_]
    return payload


@app_views.route("/cities/<city_id>/places",
                 methods=["GET", "POST"], strict_slashes=False)
def places_by_city(city_id):
    """
    Creates a new Place object
    Retrieves the list of all Place objects of a State
    Args:
        city_id: primary key of an existing Place object
    """
    city = storage.get(City, str(city_id))
    if city is None:
        abort(404)
    if request.method == "GET":
        places = {
            k: str(v) for k, v in storage.all(Place) if v.city_id == city_id}
        return jsonify([p.to_dict() for p in places.values()])
    else:
        body = request.get_json(silent=True)
        if request.is_json and body is not None:
            pay = {k: str(v) for k, v in body.items() if k in f}
            for k in f[0:2]:
                if not pay.get(k, None):
                    return jsonify({"message": "Missing " + k}), 400
            if not storage.get(User, str(pay.get("user_id"))):
                abort(404)
            pay.update({"city_id": city_id})
            new_place = Place(**(validate_payload(pay)))
            storage.new(new_place), storage.save()
            return jsonify(new_place.to_dict()), 201
        return jsonify({"message": "Not a JSON"}), 400


@app_views.route("/places/<place_id>",
                 methods=["GET", "PUT", "DELETE"], strict_slashes=False)
def one_place(place_id):
    """
    Deletes an existing City object
    Retrieves an existing City object
    Updates an existing City object
    Args:
        city_id: primary key of an existing city object
    """
    place = storage.get(Place, str(place_id))
    if not place:
        abort(404)
    if request.method == "GET":
        return place.to_dict()
    elif request.method == "DELETE":
        storage.delete(place), storage.save()
        return {}
    else:
        body = request.get_json(silent=True)
        if request.is_json and body is not None:
            pay = validate_payload(body)
            [place.__dict__.update({k: str(v)})
                for k, v in pay.items() if k in f[1:]]
            place.save()
            return jsonify(place.to_dict()), 200
        return jsonify({"message": "Not a JSON"}), 400
