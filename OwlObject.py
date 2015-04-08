from repugeng.GridObject import GridObject
from repugeng.PlayerObject import PlayerObject
from OwlTiles import OwlTiles
import random

class OwlObject(GridObject):
    """An owl.
    """
    tile="owl"
    tileset_expansion=OwlTiles
    def tick(self):
        """Your move.  If you are a creature, move!
        
        Do override if appropriate.  Default is nothing."""
        for i in range(4):
            type_=random.randrange(4)
            if type_==0: target=(self.pt[0],self.pt[1]+1)
            if type_==1: target=(self.pt[0]+1,self.pt[1])
            if type_==2: target=(self.pt[0],self.pt[1]-1)
            if type_==3: target=(self.pt[0]-1,self.pt[1])
            try: #XXX kludge/fragile/assumes
                floorlevel=type(0)(self.level.get_index_grid(*self.pt)[0][5:])
            except ValueError:
                floorlevel=1 #Needed or mazed subclass breaks
            nxtstat=self.level.get_index_grid(*target)[0]
            if self.level.objgrid[target[0]][target[1]]:
                for obj in self.level.objgrid[target[0]][target[1]][:]:
                    if isinstance(obj,PlayerObject):
                        self.level.backend.push_message("Read, or the owl will eat you")
                        break
            elif nxtstat.startswith("floor"):
                newlevel=type(0)(nxtstat[5:])
                if (newlevel-floorlevel)<=1:
                    break
            type_+=1
            type_%=4
        else: #i.e. ran to completion with no break
            return #stuck, cannot move
        self.level.objgrid[self.pt[0]][self.pt[1]].remove(self)
        self.level.objgrid[target[0]][target[1]].append(self)
        self.pt=target
        self.level.redraw()
