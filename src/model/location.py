
class Location(object):
    def __init__(self, x=0.0, y=0.0):
        self._x = x
        self._y = y

    # distance from this location to another location
    # L1 norm
    def distance_to(self, another_loc):
        return abs(self._x - another_loc.x) + abs(self._y - another_loc.y)

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    def __str__(self):
        return "location x=%f y=%f" % (self._x, self._y)
