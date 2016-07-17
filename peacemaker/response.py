import json


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
    def humans_in(self):
        if self.api_type == 'humans' and self.data.get('event_type') == 'SFIN':
            return self.data.get('measures').get('value')

    @property
    def humans_out(self):
        if self.api_type == 'humans' and self.data.get('event_type') == 'SFOUT':
            return self.data.get('measures').get('value')

    @property
    def sound(self):
        return self.data.get('extra_data').get('file_path')

    @property
    def location(self):
        return self.data.get('extra_data').get('location')
