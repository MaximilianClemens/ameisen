import logging
from .element import Element

class Hill(Element):

    def __init__(self, team: "Team", x:int, y:int, a:int):
        super().__init__(x, y, a)
        logging.debug(f'New Hill at {x}/{y}/{a}')

    def tick(self):
        super().tick()