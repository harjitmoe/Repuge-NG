from repugeng.GridObject import GridObject
from repugeng.DumbMonster import DumbMonster
from OwlTiles import OwlTiles
from OwlCorpse import OwlCorpse
import random

class OwlObject(DumbMonster):
    """An owl.
    """
    tile="owl"
    tileset_expansion=OwlTiles
    corpse_type=OwlCorpse
    name="owl"
    appearance="enormous bird"
    
