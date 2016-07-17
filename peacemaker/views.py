from flask import render_template, request

from peacemaker import app
from rejector import Rejector

devices = [{'device_id': 13, 'lat': 52.536621, 'lon': 13.4412446999999992},
           {'device_id': 14, 'lat': 48.8583, 'lon': 2.2945},
           {'device_id': 15, 'lat': 48.8583, 'lon': 2.2945}, ]


@app.route('/', methods=['GET'])
def start():
    return render_template('basic.html')


@app.route('/', methods=['POST'])
def find_location():
    latitude = request.json['latitude']
    longitude = request.json['longitude']
    rejector = Rejector((latitude, longitude), devices)
    print rejector.nearby
    return render_template('basic.html')
