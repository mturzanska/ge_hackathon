import json
import os

from flask import render_template, request, Response, url_for

from api.asset import get_audio_for_assets, get_assets
from peacemaker import app
from rejector import Rejector
from kneader import Kneader

devices = [{'device_id': 13, 'lat': 52.536621, 'lon': 13.4412446999999992},
           {'device_id': 14, 'lat': 48.8583, 'lon': 2.2945},
           {'device_id': 15, 'lat': 48.8583, 'lon': 2.2945}, ]


@app.route('/', methods=['GET'])
def start():
    print app.config['PREDIX_AUTH']
    assets_json = get_assets(app.config['PREDIX_AUTH'])
    audios = get_audio_for_assets(app.config['PREDIX_AUTH'], assets_json)
    return render_template('start.html')


@app.route('/', methods=['POST'])
def find_location():
    latitude = request.json['latitude']
    longitude = request.json['longitude']
    rejector = Rejector((latitude, longitude), devices)

# get responses for nearby devices (rejector.nearby)

    responses = [{'device_id': 1,
                  'sound': '/audio_files/getgot.mp3'},
                 {'device_id': 2,
                  'sound': '/audio_files/getgot.mp3'},
                 {'device_id': 1, 'humans_out': 12}, {'device_id': 7, 'humans_out': 7},
                 {'device_id': 1, 'humans_in': 105},
                 {'device_id': 2, 'humans_out': 1},
                 {'device_id': 2, 'humans_in': 2}]

    kneader = Kneader(responses)
    data = {'quiet': kneader.quiet,
            'empty': kneader.empty,
            'own_lat': latitude,
            'own_lon': longitude, }
    data = json.dumps(data)
    response = json.dumps({'redirect': url_for('places', data=data)})
    return Response(response=response, content_type='application/json')


@app.route('/places/<string:data>', methods=['GET'])
def places(data):
    data = json.loads(data)
    origin = data.get('own_lat'), data.get('own_lon')
    key = os.environ['GOOGLE_API_KEY']
    quiet = json.loads(data.get('quiet'))
    empty = json.loads(data.get('empty'))
    quiet_place = quiet.get('lat'), quiet.get('lon')
    empty_place = empty.get('lat'), empty.get('lon')
    units = 'imperial'
    mode = 'walking'
    return render_template('places.html', origin=origin, key=key, quiet_place=quiet_place,
                           empty_place=empty_place, units=units, mode=mode)
