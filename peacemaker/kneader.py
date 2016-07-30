from place import Place


class Kneader(object):

    def __init__(self, responses):
        # responses template [{'device_id': 3 , 'sound': 7.6 , 'humans': 15}]

        self.responses = responses
        self.full_set = self._knead()
        self.places = self._placify()
        self.quiet = self.get_place_without('noise')
        self.empty = self.get_place_without('crowd')

    def get_place_without(self, feature):
        places = self.places.values()
        get_feature = lambda x: getattr(x, feature)
        return sorted(places, key=get_feature)[0].data

    def _knead(self):
        full_set = {}
        for response in self.responses:
            device = response.pop('device_id')
            if device not in full_set:
                full_set[device] = response
            else:
                full_set[device].update(response)
        return full_set

    def _placify(self):
        places = {}
        for device, place in self.full_set.iteritems():
            place = Place(place)
            if place.noise and place.crowd:
                places[device] = place
        return places
