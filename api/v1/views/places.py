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
from . import State
from . import Amenity
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
        if value is not None:
            try:
                payload.update({_: int(value)})
            except Exception:
                del payload[_]
    for _ in f[-2:]:
        value = payload.get(_, None)
        if value is not None:
            try:
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
        abort(404, description="Not found")
    if request.method == "GET":
        places = {k: v
                  for k, v in storage.all(Place).items()
                  if v.city_id == city_id}
        return jsonify([p.to_dict() for p in places.values()])
    else:
        body = request.get_json(silent=True)
        if request.is_json and body is not None:
            pay = {k: str(v) for k, v in body.items() if k in f}
            for k in f[0:2]:
                if not pay.get(k, None):
                    abort(400, description="Missing " + k)
                if k == "user_id" and\
                        not storage.get(User, str(pay.get("user_id"))):
                    abort(404, description="Not found")
            pay.update({"city_id": city_id})
            new_place = Place(**(validate_payload(pay)))
            storage.new(new_place), storage.save()
            return jsonify(new_place.to_dict()), 201
        abort(400, description="Not a JSON")


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
        abort(404, description="Not found")
    if request.method == "GET":
        return jsonify(place.to_dict())
    elif request.method == "DELETE":
        storage.delete(place), storage.save()
        return jsonify({})
    else:
        body = request.get_json(silent=True)
        if request.is_json and body is not None:
            pay = validate_payload(body)
            [setattr(place, k, str(v)) for k, v in pay.items() if k in f[1:]]
            place.save()
            return jsonify(place.to_dict()), 200
        abort(400, description="Not a JSON")


@app_views.route("/places_search", methods=["POST"], strict_slashes=False)
def places_search():
    """
    Search for places by states and cities inclusive, filter by amenities
    """
    body = request.get_json(silent=True)
    if body is None:
        abort(400, "Not a JSON")
    states, cities, amenities = (
        body.get("states", []),
        body.get("cities", []), body.get("amenities", []))
    if body == {} or all(v == [] for v in body.values()):
        return jsonify([p.to_dict() for p in storage.all(Place).values()])
    places = []
    for sid in states:
        state = storage.get(State, sid)
        for city in state.cities:
            places.extend(city.places)
    for cid in cities:
        city = storage.get(City, cid)
        places += city.places
    amenitylist = [storage.get(Amenity, aid) for aid in amenities]
    for p in places:
        if all(amen in p.amenities for amen in amenitylist) is False:
            places.remove(p)
    return jsonify([p.to_dict() for p in places])
