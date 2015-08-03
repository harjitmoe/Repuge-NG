from CollectoInterface import CollectoInterface
from repugeng.Game import Game
from TeddyMapB import TeddyMapB
from TeddyMapG import TeddyMapG
from TeddyMapU import TeddyMapU
import random

class TeddyGame(Game):
    InterfaceClass=CollectoInterface
    leveltypes=None
    levindex=None
    _inited=0 #Int is an immutable type
    def _stack_init(self):
        if not self._inited:
            self.leveltypes=[None,TeddyMapB(self),TeddyMapG(self),TeddyMapU(self),None]
            self.levindex=1 #will be immediately +1'd by level_advance
            self._inited=1
    def level_advance(self):
        self._stack_init()
        self.levindex+=1
        self.level=self.leveltypes[self.levindex]
    def level_regress(self):
        self.levindex-=1
        self.level=self.leveltypes[self.levindex]
#
if __name__=="__main__":
    import sys
    sys.modules["TeddyGame"]=sys.modules["__main__"] #oh, Python
    TeddyGame()
