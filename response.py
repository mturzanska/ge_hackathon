import json
import os
import wget


class Response(object):

    def __init__(self, response):
        self.data = json.load(response)

    @property
    def api_type(self):
        if self.data.get('_embedded').get('medias'):
            return 'sounds'
        if self.data.get('event_type'):
            return 'humans'

    @property
    def device_id(self):
        if self.api_type == 'humans':
            return self.data.get('device-uid')
        if self.api_type == 'sounds':
            return self.data.get('_embedded').get('medias')[0].get('device-id')

    @property
    def sound(self):
        if self.api_type == 'sounds':
            sound_file = self.get_newest_media()
            return self.get_file(sound_file)

    @property
    def humans(self):
        if self.api_type == 'humans':
            return self.data.get('measures').get('value')

    @staticmethod
    def get_file(url):
        url = url.replace('http', 'https')
        filename = wget.download(url)
        cwd = os.getcwd()
        return os.path.join(cwd, filename)

    def get_newest_media(self):
        medias = []
        for media in self.data.get('_embedded').get('medias'):
            media = {'timestamp': media['timestamp'], 'url': media['url']}
            medias.append(media)
        medias = sorted(medias, key=lambda d: d['timestamp'])
        return medias[-1]['url']
