class GameOutput:

    _game: "Game"
    
    def __init__(self, game: "Game"):
        self._game = game

    def game_start(self):
        pass

    def game_tick(self):
        pass

    def game_stop(self):
        pass

    def match_start(self):
        pass

    def match_tick(self):
        pass

    def match_stop(self):
        pass
