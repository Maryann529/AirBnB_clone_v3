#!/usr/bin/python3
"""
A new view for State objects that handles all default RESTFul API actions
"""
from flask import abort
from flask import jsonify

from . import State
from . import storage
from . import app_views


@app_views.route("/states", strict_slashes=False)
def all_states():
    """
    Retrieves the list of all State objects
    """
    return jsonify([s.to_dict() for s in storage.all(State).values()])


@app_views.route("/states/<state_id>", strict_slashes=False)
def one_state(state_id):
    """
    Retrieves a State object
    """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return state.to_dict()
