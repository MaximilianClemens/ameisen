import random
from typing import Any, Type

from .config import Config
from .ameise import BaseAmeise
from .colony import Colony


from .coord import Coord

class Arena:

    _ticks: int
    
    _seed: Any
    _size: int
    _config: Config

    _elements: list
    _teams: dict

    def __init__(self, seed: Any, size:int = 5000, config: Config|None = None):
        self._ticks = 0

        self._seed = seed
        self._size = size
        self._config = config
        if not self._config:
            self._config = Config()

        self._elements = []
        self._teams = {}

        random.seed(seed)

    def _new_pos_with_distance(self, distance):
        tries = 0
        while True:
            pos_x = random.randint(0, self._size)
            pos_y = random.randint(0, self._size)
            pos_a = random.randint(0, 360)
            too_close = False
            for element in self._elements:
                if Coord.distance((pos_x, pos_y), element.get_pos()) < distance:
                    too_close = True
            
            if not too_close:
                return (pos_x, pos_y, pos_a)

            tries += 1
            if tries > 20:
                raise Exception('Too many retries')

    def add_team(self, teamname: str, *class_references:Type[BaseAmeise]):
        self._teams[teamname] = []
        for class_reference in class_references:
            new_colony = Colony(class_reference, self._new_pos_with_distance(self._config.colony_distance))
            self._teams[teamname].append(new_colony)
            self._elements.append(new_colony)


    def run(self, limit:int = 0) -> None:
        for teamname, team in self._teams.items():
            for colony in team:
                colony.spawn(self._config.start_spawn)
        
        while True:
            for element in self._elements:
                element.tick()

            self._ticks += 1
            if limit > 0 and self._ticks > limit:
                print(f'Reach tick limit')
                break
