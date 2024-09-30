from typing import Tuple
from .element import Element

class Colony(Element):
    
    def __init__(self, class_reference, pos: Tuple[int, int, int]):
        super().__init__(pos)