#!/usr/bin/python3
"""
Module for City viewa
"""
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities')
def cities_by_state(state_id):
    """ Handles GET and POST requests for City """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    if request.method == 'GET':
        cities = [city.to_dict() for city in state.cities]
        return jsonify(cities)

    if request.method == 'POST':
        data = request.get_json()
        if not data:
            abort(400, describe="Not a JSON")

        if 'name' not in data:
            abort(400, description="Missing name")

        data['state_id'] = state_id
        new_city = City(**data)
        new_city.save()
        return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>')
def city(city_id):
    """ Handles GET, DELTE and PUT requets city objects """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    if request.method == 'GEt':
        return jsonify(city.to_dict())

    if request.method == 'DELETE':
        storage.delete(city)
        storage.save()
        return jsonify({}), 200

    if request.method == 'PUT':
        data = request.get_json()
        if not data:
            abort(400, description="Not a JSON")

        for key, value in data.items():
            if key not in ['id', 'state_id', 'created_at', 'updated']:
                setattr(city, key, value)

        city.save()
        return jsonify(city.to_dict()), 200
