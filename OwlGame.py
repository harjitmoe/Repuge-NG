import sys,random,time,math
from repugeng.Game import Game
from OwlLevel import OwlLevel
from CollectoInterface import CollectoInterface

class OwlGame(Game):
    InterfaceClass=CollectoInterface
    def level_advance(self):
        self.level=OwlLevel(self)
#
if __name__=="__main__":
    OwlGame()