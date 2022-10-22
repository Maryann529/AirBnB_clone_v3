#!/usr/bin/python3
"""
A new view for User objects that handles all default RESTFul API actions
"""
from flask import abort
from flask import jsonify
from flask import request

from . import User
from . import storage
from . import app_views

# f are class properties to validate the request payload
f = ("email", "password")


@app_views.route("/users", methods=["GET", "POST"], strict_slashes=False)
def all_users():
    """
    Creates a new User object
    Retrieves the list of all User objects
    Args:
        user_id: primary key of an existing User object
    """
    if request.method == "GET":
        return jsonify([u.to_dict() for u in storage.all(User).values()])
    else:
        body = request.get_json(silent=True)
        if request.is_json and body:
            pay = {k: v for k, v in body.items() if k in f}
            for k in f:
                if not pay.get(k, None):
                    return jsonify({"message": "Missing " + k}), 400
            new_user = User(**pay)
            storage.new(new_user), storage.save()
            return jsonify(new_user.to_dict()), 201
        return jsonify({"message": "Not a JSON"}), 400


@app_views.route("/users/<user_id>",
                 methods=["GET", "PUT", "DELETE"], strict_slashes=False)
def one_user(user_id):
    """
    Deletes an existing User object
    Retrieves an existing User object
    Updates an existing User object
    Args:
        user_id: primary key of an existing User object
    """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    if request.method == "GET":
        return user.to_dict()
    elif request.method == "DELETE":
        storage.delete(user), storage.save()
        return {}
    else:
        body = request.get_json(silent=True)
        if request.is_json and body:
            [user.__dict__.update({k: v}) for k, v in body.items() if k in f]
            user.save()
            return jsonify(user.to_dict()), 200
        return jsonify({"message": "Not a JSON"}), 400
