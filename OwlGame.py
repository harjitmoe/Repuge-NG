import sys,random,time,math
from repugeng.Game import Game
from OwlLevel import OwlLevel
from CollectoInterface import CollectoInterface

class OwlGame(Game):
    InterfaceClass=CollectoInterface
    def level_initiate(self,playerobj):
        OwlLevel(self).bring_to_front(playerobj,"starting")
#
if __name__=="__main__":
    OwlGame()