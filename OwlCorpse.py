from repugeng.GridObject import GridObject
from repugeng.PlayerObject import PlayerObject
from repugeng.DumbMonster import DumbMonster
from OwlTiles import OwlTiles
import random

class OwlCorpse(GridObject):
    """An owl corpse.
    """
    tile="owl_corpse"
    tileset_expansion=OwlTiles
    name="owl corpse"
    appearance="enormous bird corpse"
    
