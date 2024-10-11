import ameisen
from clemeisen import Clemeisen

game = ameisen.Game()
game._config.seed = 'seeedy'
game.add_team('Team 1', Clemeisen)

game.run()