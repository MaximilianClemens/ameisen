from .living import Living

class BaseAmeise(Living):

    def __init__(self, x, y, a):
        super().__init__(x, y, a)

    def tick(self):
        super().tick()