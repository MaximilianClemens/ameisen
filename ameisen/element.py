from typing import Tuple

class Element:

    _pos: Tuple[int, int, int] # X, Y, A

    def __init__(self, pos: Tuple[int, int, int]):
        self._pos = pos

    def get_pos(self):
        return self._pos
    
    def on_tick(self) -> None:
        pass

    def tick(self) -> None:
        self.on_tick()