#!/usr/bin/env python
from CollectoInterface import CollectoInterface
from ludicrous.Game import Game
import random

class CollectoGame(Game):
    InterfaceClass = CollectoInterface
    leveltypes = []
    @classmethod
    def register_leveltype(cls, levelcls):
        """Add a CollectoLevel subtype to the list used by CollectoGame instances."""
        cls.leveltypes.append(levelcls)
    #
    def level_initiate(self, playerobj):
        random.choice(CollectoGame.leveltypes)(self).bring_to_front(playerobj, "starting")
    #
    def levels_reown(self):
        pass
    #
    def level_restore(self, playerobj):
        #Saving?  Never heard of it! (for now, saving only saves the levels, which
        #are completely transient anyway)
        random.choice(CollectoGame.leveltypes)(self).bring_to_front(playerobj, "starting")
    #
    def level_advance(self, playerobj):
        random.choice(CollectoGame.leveltypes)(self).bring_to_front(playerobj, "advancement")
    #
    def level_regress(self, playerobj):
        raise RuntimeError("regression in a one-way level stack")
#
if __name__ == "__main__":
    import sys
    sys.modules["CollectoGame"] = sys.modules["__main__"] #oh, Python
    import MazedCollectoLevel, DungeonCollectoLevel #BasicCollectoLevel,
    CollectoGame()
