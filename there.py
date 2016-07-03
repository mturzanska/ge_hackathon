from __future__ import division

from pydub import AudioSegment


class There(object):

    def __init__(self, sound, humans_in, humans_out):
        self.noise = self.get_noise(sound)
        self.flow = humans_in + humans_out

    @staticmethod
    def get_noise(sound):
        sound = AudioSegment.from_mp3(sound)
        noises = [milisec.dBFS for milisec in sound]
        loudest = sorted(noises, reverse=True)[:10]
        return sum(loudest)/len(loudest)
