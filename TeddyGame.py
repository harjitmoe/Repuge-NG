#!/usr/bin/env python
from CollectoInterface import CollectoInterface
from repugeng.Game import Game
from TeddyMapB import TeddyMapB
from TeddyMapG import TeddyMapG
from TeddyMapU import TeddyMapU
import random

class TeddyGame(Game):
    InterfaceClass=CollectoInterface
    use_rpc=True
    #
    leveltypes=None
    levindex=None
    _inited=0 #Int is an immutable type
    def level_initiate(self,playerobj):
        if not self._inited:
            self.leveltypes=[None,TeddyMapB(self),TeddyMapG(self),TeddyMapU(self),None]
            self._inited=1
        playerobj.levindex=2
        level=self.leveltypes[playerobj.levindex]
        level.bring_to_front(playerobj,"starting")
    def level_advance(self,playerobj):
        playerobj.levindex+=1
        level=self.leveltypes[playerobj.levindex]
        level.bring_to_front(playerobj,"advancement")
    def level_regress(self,playerobj):
        playerobj.levindex-=1
        level=self.leveltypes[playerobj.levindex]
        level.bring_to_front(playerobj,"regression")
#
if __name__=="__main__":
    import sys
    sys.modules["TeddyGame"]=sys.modules["__main__"] #oh, Python
    TeddyGame()
