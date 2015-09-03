from repugeng.GridObject import GridObject
from repugeng.DijkstraMonster import DijkstraMonster
from OwlCorpse import OwlCorpse
import random

class OwlObject(DijkstraMonster):
    """An owl.
    """
    tile="owl"
    corpse_type=OwlCorpse
    name="owl"
    appearance="enormous bird"
    
