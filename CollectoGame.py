from prelevula.MazeLevel import MazeLevel
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
    def level_advance(self):
        return random.choice(CollectoGame.leveltypes)(self,1)
#
if __name__=="__main__":
    import sys
    sys.modules["CollectoGame"]=sys.modules["__main__"] #oh, Python
    import MazedCollectoLevel,DungeonCollectoLevel#BasicCollectoLevel,
    CollectoGame()
