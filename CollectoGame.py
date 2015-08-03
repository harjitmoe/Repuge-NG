from prelevula.MazeLevel import MazeLevel
from CollectoInterface import CollectoInterface
from repugeng.Game import Game
import random

class CollectoGame(Game):
    InterfaceClass=CollectoInterface
    _leveltypes=[]
    @classmethod
    def register_leveltype(cls,subcls):
        cls._leveltypes.append(subcls)
    @classmethod
    def get_next_leveltype(cls):
        return random.choice(cls._leveltypes)
    #
    def gen_next_level(self):
        return CollectoGame.get_next_leveltype()() #yes, two ()
#
if __name__=="__main__":
    import sys
    sys.modules["CollectoGame"]=sys.modules["__main__"] #oh, Python
    import MazedCollectoGame,DungeonCollectoGame#BasicCollectoGame,
    CollectoGame()

