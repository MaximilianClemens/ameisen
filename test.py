import ameisen
from clemeisen import Clemeisen

game = ameisen.Game()
#game._config.seed = 'seeedy'
game.add_team('Team A', Clemeisen)
game.add_team('Team B', Clemeisen)

game.start()