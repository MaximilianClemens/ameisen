from .hill import Hill
from .ameise import BaseAmeise
from typing import Any, Type
import logging

class Team:

    _game: "Game"
    _race: Type[BaseAmeise]
    _teamname: str
    _racename: str
    _hill: Hill

    def __init__(self, game: "Game", teamname:str, race:Type[BaseAmeise]):
        self._game = game
        self._race = race
        self._racename = self._race.__name__
        self._teamname = teamname

    def setup(self):
        logging.debug(f'Setup Team: {self._teamname} Race: {self._racename}')
        coords = self._game.get_new_hill_coords()
        self._hill = Hill(self, *coords)
        self._game.register_element(self._hill)

    def tick(self):
        pass