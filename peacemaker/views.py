import json
import os

from flask import render_template, request, Response, url_for

from peacemaker import app
from rejector import Rejector

devices = [{'device_id': 13, 'lat': 52.536621, 'lon': 13.4412446999999992},
           {'device_id': 14, 'lat': 48.8583, 'lon': 2.2945},
           {'device_id': 15, 'lat': 48.8583, 'lon': 2.2945}, ]


@app.route('/', methods=['GET'])
def start():
    return render_template('start.html')


@app.route('/', methods=['POST'])
def find_location():
    latitude = request.json['latitude']
    longitude = request.json['longitude']
    rejector = Rejector((latitude, longitude), devices)
    data = {'places': rejector.nearby,
            'own_lat': latitude,
            'own_lon': longitude, }
    data = json.dumps(data)
    response = json.dumps({'redirect': url_for('places', data=data)})
    print response
    return Response(response=response, content_type='application/json')


@app.route('/places/<string:data>', methods=['GET'])
def places(data):
    data = json.loads(data)
    origin = data.get('own_lat'), data.get('own_lon')
    key = os.environ['GOOGLE_API_KEY']
    a_place = data.get('places')[0]
    destination = a_place.get('lat'), a_place.get('lon')
    units = 'imperial'
    mode = 'walking'
    return render_template('places.html', origin=origin, key=key, destination=destination,
                           units=units, mode=mode)
