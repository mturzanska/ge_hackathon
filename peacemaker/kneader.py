from place import Place


class Kneader(object):

    def __init__(self, responses):
        # responses template [{'device_id': 3 , 'lat': 6.777, 'lon': 3.44,
        #                      'sound': 7.6 , 'humans': 15}]

        self.responses = responses
        self.full_set = self._knead()
        self.places = self._placify()
        self.quiet = self.get_place_without('noise')
        self.secluded = self.get_place_without('crowd')

    def get_place_without(self, feature):
        places = self.places.values()
        get_feature = lambda x: getattr(x, feature)
        try:
            return sorted(places, key=get_feature)[0].data
        except IndexError:
            return {}

    def _knead(self):
        full_set = {}
        for response in self.responses:
            dev_id = response.get('device_id')
            if dev_id not in full_set:
                full_set[dev_id] = response
            else:
                full_set[dev_id].update(response)
        return full_set

    def _placify(self):
        places = {}
        for device, place in self.full_set.iteritems():
            place = Place(place)
            if place.noise and place.crowd:
                places[device] = place
        return places
