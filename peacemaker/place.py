from __future__ import division
import json

from pydub import AudioSegment


class Place(object):
    # place template {'sound': 7.5, 'humans_out': 12, 'humans_in': 3}

    def __init__(self, place):
        self.place = place
        self.lat = place.get('lat')
        self.lon = place.get('lon')
        self.crowd = self.get_crowd(self.place.get('humans_in'),
                                    self.place.get('humans_out'))
        self.noise = self.get_noise(self.place.get('sound'))
        self.data = self.jsonify()

    @staticmethod
    def get_noise(sound_file):
        if sound_file:
            sound = AudioSegment.from_mp3(sound_file)
            noises = [milisec.dBFS for milisec in sound]
            index = min(10, len(noises))
            loudest = sorted(noises, reverse=True)[:index]
            return sum(loudest)/len(loudest)

    @staticmethod
    def get_crowd(humans_in, humans_out):
        if humans_in and humans_out:
            return humans_in + humans_out
        if humans_in and not humans_out:
            return humans_in
        if humans_out and not humans_in:
            return humans_out

    def jsonify(self):
        attrs = {'noise': self.noise,
                 'flow': self.crowd,
                 'lat': self.lat,
                 'lon': self.lon}
        return json.dumps(attrs)
