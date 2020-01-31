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
    #states_objs = storage.all('Victim').values()
    #index = 0
    #for element in states_objs:
     #   cities_list.append(element.to_dict())
     #    cities_list[index]['name'] = storage.get('State', element.state_id).name
      #  index += 1
    victims_list.append(storage.exec())
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
    state_obj = storage.get('State', state_id)
    if state_obj is None:
        abort(404)
    city_data = request.get_json()
    print(city_data)
    if city_data is None:
        abort(400, "Not a JSON")
    if not city_data.get('value'):
        abort(400, "Missing value")
    city_data['state_id'] = state_id
    new_victim = Victim(**city_data)
    storage.new(new_victim)
    storage.save()
    storage.reload()
    return make_response(jsonify(new_victim.to_dict())), 201

