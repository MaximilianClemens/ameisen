from typing import Tuple

import math

class Coord:

    @staticmethod
    def distance(self, pos1, pos2):
        distance_x = None
        distance_y = None

        distance_x = max(pos1[0], pos2[0]) - min(pos1[0], pos2[0])
        distance_y = max(pos1[1], pos2[1]) - min(pos1[1], pos2[1])

        return math.hypot(distance_x, distance_y)