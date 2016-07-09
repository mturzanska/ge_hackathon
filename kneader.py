from there import There


class Kneader(object):

    def __init__(self, responses):
        # resopnses template [{'device_id': 3 , 'sound': 7.6 , 'humans': 15}, ]
        self.responses = responses
        self.places = self.knead()
        self.theres = self.thereify()

    def knead(self):
        places = {}
        for response in self.responses:
            device = response.pop('device_id')
            if device not in places:
                places[device] = response
            else:
                places[device].update(response)
        return places

    def thereify(self):
        places_cracked = {}
        for device, place in self.places.iteritems():
            place_cracked = There(place)
            places_cracked[device] = place_cracked
        return places_cracked
