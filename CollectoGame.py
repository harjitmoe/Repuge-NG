#!/usr/bin/env python
from CollectoInterface import CollectoInterface
from repugeng.Game import Game
import random

class CollectoGame(Game):
    InterfaceClass=CollectoInterface
    leveltypes=[]
    @classmethod
    def register_leveltype(cls,levelcls):
        cls.leveltypes.append(levelcls)
    #
    def level_initiate(self,playerobj):
        random.choice(CollectoGame.leveltypes)(self).bring_to_front(playerobj,"starting")
    #
    def level_advance(self,playerobj):
        random.choice(CollectoGame.leveltypes)(self).bring_to_front(playerobj,"advancement")
#
if __name__=="__main__":
    import sys
    sys.modules["CollectoGame"]=sys.modules["__main__"] #oh, Python
    import MazedCollectoLevel,DungeonCollectoLevel#BasicCollectoLevel,
    CollectoGame()
