from .element import Element

class Living(Element):

    _alive: bool
    _health: int
    _speed: int

    def __init__(self, x, y, a, health, speed):
        super().__init__(x, y, a)

        self._alive = True
        self._health = health
        self._speed = speed

        self.on_hatching()

    def tick(self):
        """ Called on every gametick, internal function """

        super().tick()
        self.on_tick()

    def on_hatching(self):
        """ Called when the Living is born """
        pass

    def on_tick(self):
        """ Called on every gametick """
        pass

    