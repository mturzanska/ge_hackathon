import json
import os

from flask import render_template, request, Response, url_for

from api.asset import (
    get_audio_for_assets, get_audio_assets, get_pedestrian_event_assets,
    get_pedestrians_for_assets)

from peacemaker import app
from rejector import Rejector
from kneader import Kneader

devices = [{'device_id': 13, 'lat': 52.536621, 'lon': 13.4412446999999992},
           {'device_id': 12, 'lat': 52.536621, 'lon': 13.4412446999999992},
           {'device_id': 14, 'lat': 48.8583, 'lon': 2.2945},
           {'device_id': 15, 'lat': 48.8583, 'lon': 2.2945}]

responses = [{'device_id': 13,
              'sound': '/Users/malgorzataturzanska/Prirepos/GE_Hackathon/audio_files/getgot.mp3',
              'lat': 52.5366,
              'lon': 13.44},
             {'device_id': 13, 'humans_out': 12, 'lat': 52.5366, 'lon': 13.44},
             {'device_id': 13, 'humans_in': 105, 'lat': 52.5366, 'lon': 13.44},
             {'device_id': 12, 'humans_out': 1, 'lat': 52.5366, 'lon': 13.44},
             {'device_id': 12, 'humans_in': 2, 'lat': 52.5366, 'lon': 13.44}]


@app.route('/', methods=['GET'])
def start():
    # api examples
    # assets_json = get_audio_assets(app.config['SAFETY_AUTH'])
    # audio_file_paths = get_audio_for_assets(app.config['SAFETY_AUTH'],
                                            # assets_json)
    # print audio_file_paths

    # assets_json = get_pedestrian_event_assets(app.config['PEDESTRIAN_AUTH'])
    # pedestrian_avgs = get_pedestrians_for_assets(app.config['PEDESTRIAN_AUTH'],
                                                 # assets_json)
    # print pedestrian_avgs
    return render_template('start.html')


@app.route('/', methods=['POST'])
def find_location():
    latitude = request.json['latitude']
    longitude = request.json['longitude']
    rejector = Rejector((latitude, longitude), devices)
    # get responses for nearby devices (rejector.nearby)
    kneader = Kneader(responses)
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
        quiet_loc = quiet.get('lat'), quiet.get('lon')
    secluded = data.get('secluded')
    if secluded:
        secluded = json.loads(secluded)
        secluded_loc = secluded.get('lat'), secluded.get('lon')
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
