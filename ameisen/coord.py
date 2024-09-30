from typing import Tuple

import math

class Coord:

    """ Ueberlegungen zur Distanz
        AmeisenLaenge = 4
        BauDurchmesser = inital:200, kann wachsen
        Kaefer = 12
        Apfel = 20
        Zuckerhaufen = 24

        Jeder Tick = 1 Schritt?
    """


    @staticmethod
    def distance(self, pos1, pos2):
        distance_x = None
        distance_y = None

        distance_x = max(pos1[0], pos2[0]) - min(pos1[0], pos2[0])
        distance_y = max(pos1[1], pos2[1]) - min(pos1[1], pos2[1])

        return math.hypot(distance_x, distance_y)