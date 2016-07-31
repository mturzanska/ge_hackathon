from math import acos, cos, pi, sin


class Rejector(object):

    SEARCH_RADIUS = 5  # km

    def __init__(self, location, devices):
        self.own_lat = location[0] * pi/180
        self.own_lon = location[1] * pi/180
        self.nearby = self.reject_distant(devices)

    @staticmethod
    def get_distance(lat1, lon1, lat2, lon2, earth_radius=6371):
        return acos(sin(lat1) * sin(lat2) + cos(lat1) * cos(lat2)
                    * cos(lon1 - lon2)) * earth_radius

    def reject_distant(self, devices):
        nearby = []
        for device in devices:
            for device_id, data in device.iteritems():
                lat = float(data.get('location').get('lat')) * pi/180
                lon = float(data.get('location').get('lng')) * pi/180
                distance = self.get_distance(self.own_lat, self.own_lon, lat, lon)
                if distance <= self.SEARCH_RADIUS:
                    nearby.append(device)
        return nearby
