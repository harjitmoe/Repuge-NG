from repugeng.GridObject import GridObject
from repugeng.DijkstraMonster import DijkstraMonster
from OwlTiles import OwlTiles
from OwlCorpse import OwlCorpse
import random

class OwlObject(DijkstraMonster):
    """An owl.
    """
    tile="owl"
    tileset_expansion=OwlTiles
    corpse_type=OwlCorpse
    name="owl"
    appearance="enormous bird"
    
