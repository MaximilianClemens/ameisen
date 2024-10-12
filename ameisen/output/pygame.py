import pygame
import logging
import pathlib

from . import GameOutput

from ..hill import Hill

class Color:
    GREY = pygame.Color(128, 128, 128)
    RED = pygame.Color(255, 0, 0)
    WHITE = pygame.Color(255, 255, 255)
    BLACK = pygame.Color(0, 0, 0)
    GOLD = pygame.Color(255, 215, 0)
    SAND = pygame.Color(240, 237, 221)

# Shortcuts
C=Color

class PygameOutput(GameOutput):

    _zoom: int
    #_camera_x: int
    #_camera_y: int

    _moving: bool
    
    def game_start(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self._game._config.window_width, self._game._config.window_height))
        pygame.display.set_caption("Ameisen")
        pygame.font.init()
        #pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.MOUSEWHEEL, pygame.MOUSEMOTION])

        current_path = pathlib.Path(__file__).parent.resolve()
        self.img_hill = pygame.image.load(f'{current_path}/hill.png')
        #self.img_ant = pygame.image.load('ant.png')

        # self.font_headline = pygame.font.SysFont('Comic Sans MS', 30)
        # self.font_subline = pygame.font.SysFont('Comic Sans MS', 20)

    def _add_text(self, pos, text, size=20, color=C.BLACK, font='Calibri'):
        font_o = pygame.font.SysFont(font, size)
        #font_o = pygame.font.SysFont('Comic Sans MS', 30)
        text_o = font_o.render(text, False, color)
        self.screen.blit(text_o, pos)

    # def _tick(self):
    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             self._game._game_run = False
    #         elif event.type == pygame.MOUSEWHEEL:
    #             if event.y == -1:
    #                 # raus zoomen
    #                 logging.debug('raus')
    #             elif event.y == 1:
    #                 # rein zoomen
    #                 logging.debug('rein')
    #         elif event.type == pygame.KEYDOWN:
    #             if event.key == pygame.K_LEFT:
    #                 logging.debug('links')
    #             elif event.key == pygame.K_RIGHT:
    #                 logging.debug('rechts')
    #             elif event.key == pygame.K_UP:
    #                 logging.debug('hoch')
    #             elif event.key == pygame.K_DOWN:
    #                 logging.debug('runter')
    #             elif event.key == pygame.K_ESCAPE:
    #                 logging.debug('escape')

    #     pygame.display.update()

    # Game Functions

    def _game_tick_handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._game._game_run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self._game._match_run = True

    def game_tick(self):

        self._game_tick_handle_events()

        self.screen.fill(C.GREY)
        self._add_text((10, 0), 'Ameisen', 30)
        self._add_text((10, 50), 'Press ESC to start match', 15)

        self._add_text((50, 90), 'Match participants', 20, color=C.GOLD)

        offset = 130
        participant_size = 15

        for team, teamclass in self._game._game_teams.items():
            class_name = teamclass.__name__
            self._add_text((65, offset), f'{team} with {class_name}', participant_size)
            offset += participant_size + int(participant_size/2)
        

        pygame.display.update()

    def game_stop(self):
        pygame.quit()


    # Match Functions
    def _match_tick_handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Exit Game
                self._game._game_run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._moving = True
            elif event.type == pygame.MOUSEBUTTONUP:
                self._moving = False
            elif event.type == pygame.MOUSEMOTION and self._moving:
                self._offset_x += event.rel[0]
                self._offset_y += event.rel[1]
            elif event.type == pygame.MOUSEWHEEL:

                if event.y == -1:
                    self._zoom -= 0.5
                elif event.y == 1:
                    self._zoom += 0.5
                
                if self._zoom < 1:
                    self._zoom = 1
                
                # print(self._zoom)
                
                # print(pygame.mouse.get_pos())

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # Exit Match
                    self._game._match_run = False
                elif event.key == pygame.K_F1:
                    self._game._match_pause = not self._game._match_pause
                    if self._game._match_pause:
                        logging.info('Match paused')
                    else:
                        logging.info('Match resumed')
                elif event.key == pygame.K_SPACE:
                    self._offset_x = self._inital_offset_x
                    self._offset_y = self._inital_offset_y
                    self._moving = False
                    self._zoom = 1

    def match_start(self):
        # Only called Once
        self._moving = False
        self._zoom = 1
        self._offset_x = 0
        self._offset_y = 0
        
        self._ratio = min(self._game._config.window_height, self._game._config.window_width) / self._game._config.map_size
        self._inital_offset_x = (self._game._config.window_width - self._game._config.window_height) / 2
        self._inital_offset_y = (self._game._config.window_height - self._game._config.window_width) / 2

        logging.info(f'Window to Map Ratio = {self._ratio}')

        if self._inital_offset_y < 0:
            self._inital_offset_y = 0
        
        if self._inital_offset_x < 0:
            self._inital_offset_x = 0

        self._offset_x = self._inital_offset_x
        self._offset_y = self._inital_offset_y

        #self.screen.fill(C.SAND)
        pygame.display.update()

    def _draw_match(self) -> pygame.Surface:
        gamefield = pygame.Surface((self._game._config.map_size, self._game._config.map_size))
        gamefield.fill(C.SAND)

        # Draw Hills
        for hill in self._game.get_elements_of_type(Hill):
            gamefield.blit(self.img_hill, (hill.x,hill.y))

        return gamefield

    def match_tick(self):
        self._match_tick_handle_events()
        self.screen.fill(C.WHITE)

        gamefield = self._draw_match() # wir malen das FELD
        gamefield_scaled = pygame.transform.scale_by(gamefield, self._ratio*self._zoom)

        self.screen.blit(gamefield_scaled, (self._offset_x*self._zoom, self._offset_y*self._zoom))
        

        # gamefield_scaled = pygame.transform.scale_by(gamefield, self._ratio) #_ratio
        
        # gamefield_oversize = pygame.Surface((self._game._config.window_width, self._game._config.window_height))
        # gamefield_oversize.fill(C.GREY)
        # gamefield_oversize.blit(gamefield_scaled, (self._inital_offset_x, self._inital_offset_y))

        # gamefield_oversize_scaled = pygame.transform.scale_by(gamefield_oversize, self._zoom) #_zoom
        
        # gamefield_oversize_scaled_scroll = pygame.Surface((self._game._config.window_width, self._game._config.window_height))
        # gamefield_oversize_scaled_scroll.blit(gamefield_oversize_scaled, (self._offset_x, self._offset_y))

        # ####gamefield_oversize_scaled.scroll(self._offset_x, self._offset_y)
        
        # self.screen.blit(gamefield_oversize_scaled_scroll, (0,0))
        

        pygame.display.update()

    def match_stop(self):
        pass
