import sys,random,time,math
from repugeng.Game import Game
from OwlLevel import OwlLevel
from CollectoInterface import CollectoInterface

class OwlGame(Game):
    InterfaceClass=CollectoInterface
    #use_rpc=True
    lev=None
    def level_initiate(self,playerobj):
        self.lev=OwlLevel(self)
        self.lev.bring_to_front(playerobj,"starting")
#
if __name__=="__main__":
    OwlGame()