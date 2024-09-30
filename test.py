import ameisen

from clemeisen import Clemeisen


arena = ameisen.Arena(
    seed='HALLOWELT',
    size=5
)

arena.add_team('Team Max', Clemeisen)

arena.run(limit = 1000)

