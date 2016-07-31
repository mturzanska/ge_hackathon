from __future__ import division
import json

from pydub import AudioSegment


class Place(object):
    def __init__(self, place):
        self.place = place
        self.lat = place.get('location').get('lat')
        self.lng = place.get('location').get('lng')
        self.crowd = self.place.get('pedestrians')
        self.noise = self.get_noise(self.place.get('audio_path'))
        self.data = self.jsonify()

    @staticmethod
    def get_noise(sound_file):
        if sound_file:
            sound = AudioSegment.from_mp3(sound_file)
            noises = [milisec.dBFS for milisec in sound]
            index = min(10, len(noises))
            loudest = sorted(noises, reverse=True)[:index]
            return sum(loudest)/len(loudest)

    def jsonify(self):
        attrs = {'noise': self.noise,
                 'flow': self.crowd,
                 'lat': self.lat,
                 'lng': self.lng}
        return json.dumps(attrs)
