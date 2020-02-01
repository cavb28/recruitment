#!/usr/bin/python3
"""States view module.."""
import pandas as pd
from models import storage
from models.victim import Victim
from models.state import State
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request, make_response, render_template
from itertools import groupby


@app_views.route('/victims', methods=['GET'], strict_slashes=False)
def all_victims():
    """Retrieves the list of all State objects"""
    victims_list = []
    victims_objs = storage.all('Victim').values()
    index = 0
    for element in victims_objs:
        victims_list.append(element.to_dict())
        victims_list[index]['name'] = storage.get('State', element.state_id).name
        index += 1

    return jsonify(victims_list)


@app_views.route('/states/<state_id>/victims',
                 methods=['GET'], strict_slashes=False)
def victims_list(state_id):
    """Retrieves the list of all State objects"""
    cities_list = []
    cities_objs = storage.get('State', state_id)
    if cities_objs is None:
        abort(404)
    for city in cities_objs.victims:
        cities_list.append(city.to_dict())

    return jsonify(cities_list)


@app_views.route('/states/<state_id>/victims',
                 methods=['POST'], strict_slashes=False)
def new_city(state_id):
    """Creates a new state"""
    victim = {}
    state_obj = storage.get('State', state_id)

    if state_obj is None:
        abort(404)
    city_data = request.get_json()
    if city_data is None:
        abort(400, "Not a JSON")
    if not city_data.get('value'):
        abort(400, "Missing value")
    city_data['state_id'] = state_id
    for element in state_obj.victims:
        if element.state_id == state_id:
            victim = element.to_dict()
    print(victim)
    if not victim:
        new_victim = Victim(**city_data)
        storage.new(new_victim)
        storage.save()
        storage.reload()
        return make_response(jsonify(new_victim.to_dict())), 201
    else:
        victim_update = storage.get('Victim', victim.get('id'))
        victim_val = int(city_data['value']) + int(victim.get('value'))
        setattr(victim_update, 'value', victim_val)
        victim_update.save()
        return make_response(jsonify(victim_update.to_dict())), 201
