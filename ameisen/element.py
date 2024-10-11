class Element:

    _x: int
    _y: int
    _a: int

    def __init__(self, x:int, y:int, a:int):
        self._x = x
        self._y = y
        self._a = a

    def tick(self):
        pass