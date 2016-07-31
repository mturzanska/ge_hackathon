import json
import os

from flask import render_template, request, Response, url_for

from api.asset import (
    get_audio_for_assets, get_audio_assets, get_pedestrian_event_assets,
    get_pedestrians_for_assets)

from peacemaker import app
from rejector import Rejector
from kneader import Kneader


@app.route('/', methods=['GET'])
def start():
    return render_template('start.html')


@app.route('/', methods=['POST'])
def find_location():
    latitude = request.json['latitude']
    longitude = request.json['longitude']
    assets_json = get_audio_assets(app.config['SAFETY_AUTH'])
    audio_file_paths = get_audio_for_assets(app.config['SAFETY_AUTH'],
                                            assets_json)
    assets_json = get_pedestrian_event_assets(app.config['PEDESTRIAN_AUTH'])
    pedestrian_avgs = get_pedestrians_for_assets(app.config['PEDESTRIAN_AUTH'],
                                                 assets_json)
    responses = audio_file_paths + pedestrian_avgs
    rejector = Rejector((latitude, longitude), responses)
    kneader = Kneader(rejector.nearby)
    data = {'quiet': getattr(kneader, 'quiet', None),
            'secluded': getattr(kneader, 'secluded', None),
            'own_lat': latitude,
            'own_lon': longitude}
    data = json.dumps(data)
    response = json.dumps({'redirect': url_for('places', data=data)})
    return Response(response=response, content_type='application/json')


@app.route('/places/<string:data>', methods=['GET'])
def places(data):
    data = json.loads(data)
    quiet = data.get('quiet')
    if quiet:
        quiet = json.loads(quiet)
        quiet_loc = float(quiet.get('lat')), float(quiet.get('lng'))
    secluded = data.get('secluded')
    if secluded:
        secluded = json.loads(secluded)
        secluded_loc = float(secluded.get('lat')), float(secluded.get('lng'))
    if quiet and secluded and quiet == secluded:
        places = {'Quiet and secluded': quiet_loc}
    elif not quiet and secluded:
        places = {'Secluded': secluded_loc}
    elif quiet and not secluded:
        places = {'Quiet': quiet_loc}
    elif not quiet and not secluded:
        places = {}
    else:
        places = {'Quiet': quiet_loc,
                  'Secluded': secluded_loc}
    origin = data.get('own_lat'), data.get('own_lon')
    key = os.environ['GOOGLE_API_KEY']
    units = 'imperial'
    mode = 'walking'
    return render_template('places.html', origin=origin, key=key, places=places,
                           units=units, mode=mode)
