from place import Place


class Kneader(object):

    def __init__(self, responses):
        self.responses = responses
        self.full_set = self._knead()
        self.places = self._placify()
        self.quiet = self.get_place_without('noise')
        self.secluded = self.get_place_without('crowd')

    def get_place_without(self, feature):
        places = self.places.values()
        places = [pl for pl in places if getattr(pl, feature) is not None]
        get_feature = lambda x: getattr(x, feature)
        try:
            return sorted(places, key=get_feature)[0].data
        except IndexError:
            return {}

    def _knead(self):
        full_set = {}
        for response in self.responses:
            for device, data in response.iteritems():
                if device not in full_set:
                    full_set[device] = data
                else:
                    full_set[device].update(data)
        return full_set

    def _placify(self):
        places = {}
        for device, place in self.full_set.iteritems():
            place = Place(place)
            if place.noise or place.crowd:
                places[device] = place
        return places
