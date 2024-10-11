import logging
import random
import pygame

from typing import List, Any, Type

from .team import Team
from .config import Config
from .ameise import BaseAmeise
from .element import Element
from .hill import Hill

from .coordinator import Coordinator

class Game:

    _run: bool
    _ticks: int
    _teams: List[Team]
    _elements: List[Element]
    
    _config: Config | None

    def __init__(self, config: Config | None = None):
        self._run = False
        self._ticks = 0
        self._teams = list()
        self._elements = list()
        
        self._config = config
        if not self._config:
            self._config = Config()

        logging.basicConfig(
            format="[{asctime}] {levelname}: {message}",
            style="{",
            datefmt="%Y-%m-%d %H:%M",
            level=logging.DEBUG,
        )

    def add_team(self, teamname:str, race:Type[BaseAmeise]):
        self._teams.append(Team(self, teamname, race))

    def run(self, limit:int = 0):
        logging.info('Starting Game')

        self._run = True
        self._ticks = 0

        self._setup()

        while self._run:
            self._tick()

            if limit > 0 and self._ticks >= limit:
                self._run = False
        
        self._end()

    def _setup(self):
        logging.debug('Setup Game')

        # GUI init
        pygame.init()
        pygame.display.set_mode((640, 480))
        pygame.display.set_caption("Ameisen")
        
        if not self._config.seed:
            self._config.seed = random.randint(0,999999)
        
        random.seed(self._config.seed)
        logging.debug(f'Seed = {type(self._config.seed).__name__}:{self._config.seed}')

        # create Hills
        for team in self._teams:
            team.setup()
    
    def _end(self):
        logging.debug('End Game')

    def _tick(self):
        self._ticks += 1

        # Handle GUI events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._run = False
            elif event.type == pygame.MOUSEWHEEL:
                if event.y == -1:
                    # raus zoomen
                    logging.debug('raus')
                elif event.y == 1:
                    # rein zoomen
                    logging.debug('rein')
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    logging.debug('links')
                elif event.key == pygame.K_RIGHT:
                    logging.debug('rechts')
                elif event.key == pygame.K_UP:
                    logging.debug('hoch')
                elif event.key == pygame.K_DOWN:
                    logging.debug('runter')

        # Game Logic
        for team in self._teams:
            team.tick()

        # Gui Logic
        screen.fill(WEISS)

    def register_element(self, element: Element):
        self._elements.append(element)

    def get_elements_of_type(self, type: Type[Element]):
        for element in self._elements:
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