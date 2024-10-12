import logging
import random

from typing import List, Any, Type

from .team import Team
from .config import Config
from .ameise import BaseAmeise
from .element import Element
from .hill import Hill

from .coordinator import Coordinator
from .output import GameOutput
from .output.pygame import PygameOutput

class Game:

    _game_run: bool # Game run
    _game_teams: dict
    
    _match_run: bool # Match run
    _match_pause: bool
    
    _match_ticks: int
    _match_teams: List[Team]
    _match_elements: List[Element]

    _output: Type[GameOutput] | None
    
    _config: Config | None

    def __init__(self, config: Config | None = None, output: Type[GameOutput]|None = None):

        # Initialize Vars
        self._game_run = False
        self._game_teams = {}
        
        self._match_run = False
        self._match_pause = False
        self._match_ticks = 0
        self._match_teams = []
        self._match_elements = []

        # Initialize Config
        self._config = config
        if not self._config:
            self._config = Config()

        # Initialize GameOutput
        if not output:
            self._output = PygameOutput(self)
        else:
            self._output = output(self)
        
        # Initialize Logger
        logging.basicConfig(
            format="[{asctime}] {levelname}: {message}",
            style="{",
            datefmt="%Y-%m-%d %H:%M",
            level=logging.DEBUG,
        )

    def start(self):
        logging.info('Starting Game')
        self._game_start()

    def _game_start(self):
        if len(self._game_teams) == 0:
            logging.error('Please add at least one Team!')
            return

        self._game_run = True
        self._output.game_start()

        while self._game_run:
            self._game_tick()
        
        self._game_stop()

    def _game_tick(self):
        self._output.game_tick()

        if self._match_run:
            self._match_start()

            while self._match_run and self._game_run:
                self._match_tick()

            self._match_stop()

    def _game_stop(self):
        logging.info('Stopping Game')
        self._output.game_stop()
 
    def _match_start(self):
        logging.info('Starting Match')
        
        # Reset Match vars
        self._match_ticks = 0
        self._match_teams = []
        self._match_elements = []

        # Generate random Seed if not set
        if not self._config.seed:
            seed = random.randint(0,999999)
        else:
            seed = self._config.see
        
        # Enable Seed
        random.seed(seed)
        logging.debug(f'Seed = {type(self._config.seed).__name__}:{self._config.seed}')

        for team, teamclass in self._game_teams.items():
            team_object = Team(self, team, teamclass)
            self._match_teams.append(team_object)
            team_object.setup()

        self._output.match_start()

    def _match_tick(self):
        self._output.match_tick()

        self._match_ticks += 1

    def _match_stop(self):
        logging.info('Stopping Match')
        self._output.match_stop()

    # General Funcs

    def add_team(self, teamname:str, race:Type[BaseAmeise]):
        self._game_teams[teamname] = race

    # Element Functions

    def register_element(self, element: Element):
        self._match_elements.append(element)

    def get_elements_of_type(self, type: Type[Element]):
        for element in self._match_elements:
            if isinstance(element, type):
                yield element
    
    def get_new_hill_coords(self):
        tries = 0
        while tries < 20:
            tries += 1

            x = random.randint(0, self._config.map_size)
            y = random.randint(0, self._config.map_size)
            a = random.randint(0, 360)

            too_close = False

            for hill in self.get_elements_of_type(Hill):
                if Coordinator.distance((x, y), (hill.x, hill.y)) < self._config.hill_distance:
                    too_close = True
                    break
            
            if not too_close:
                return [x, y, a]

        raise Exception('Too many retries')

