from .element import Element

from .living import Living

class BaseAmeise(Living):

    _pos:tuple[int, int, int] # X, Y, A
    _health: int
    _max_load: int
    _max_reach: int
    
    _load = None



    def __init__(self, id:int, parent: Element):
        self

    def tick(self):
        super().tick()

    # debug

    def on_hatching(self):
        """ Triggered when the Ant births/hatches """
        pass

    def think(self, message):
        """ Debug Message """
        super().think(message)

    # getters

    def get_distance(self, element):
        pass

    def get_distance_home(self):
        pass

    def get_current_load(self):
        pass

    def get_reach(self):
        pass

    # Movers

    def move_forward(self, steps:int = 0):
        """ The Ant will move forward """
        pass

    def move_to(self, element):
        """ The Ant will move to element """
        pass

    def move_home(self):
        """ The Ant will move home """
        pass

    # Doers

    def take(self, element, amount):
        """ The Ant will take amount of element, if possible """
        pass

    def mark(self, information: tuple[int, int, int]):
        pass
    
    # Callbacks

    def on_wait(self) -> None:
        """ This Method is called, when the Ant does nothing """
        pass

    def on_tired(self) -> None:
        """ This Method is called, when the Ant is tired """
        pass

    def on_move(self) -> None:
        pass

    def on_sees(self, element) -> None:
        """ This Method is called, when the Ant sees an element """
        pass

    def on_touches(self, element) -> None:
        """ This Method is called, when the Ant touch an element """
        pass

    def on_target(self, element) -> None:
        """ This Method is called, when the Ant reach its target """
        pass

    def on_tick(self) -> None:
        pass

    def on_smells(self, mark) -> None:
        """ Ant can only smell friedly marks """
        pass