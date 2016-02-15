from ludicrous.GridObject import GridObject
from ludicrous.DijkstraMonster import DijkstraMonster
from OwlCorpse import OwlCorpse
import random

class OwlObject(DijkstraMonster):
    """An owl.
    """
    tile="owl"
    corpse_type=OwlCorpse
    name="owl"
    appearance="enormous bird"
    projectiles=1
    priority=1
    def initialise(self):
        super(OwlObject,self).initialise()
        self.insert(GridObject(self.level))
        self.insert(GridObject(self.level))
        self.insert(GridObject(self.level))
