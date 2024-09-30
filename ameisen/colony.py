import random

from typing import Tuple, Type
from .element import Element
from copy import deepcopy
from .ameise import BaseAmeise

class Colony(Element):

    _ants: list[BaseAmeise]
    _class_reference: Type[BaseAmeise]
    
    def __init__(self, class_reference, pos: Tuple[int, int, int]):
        super().__init__(pos)
        self._class_reference = class_reference
        self._ants = []

    def spawn(self, amount:int):
        for i in range(0, amount):
            pos = (
                self._pos[0],
                self._pos[1],
                random.randint(0, 360)
            )
            self._ants.append(self._class_reference(pos, self))

    def on_tick(self):
        for ant in self._ants:
            ant.tick()
            
