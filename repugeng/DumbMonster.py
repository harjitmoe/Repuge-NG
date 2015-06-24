from repugeng.GridObject import GridObject
from repugeng.PlayableObject import PlayableObject
from repugeng.Container import Container
import random

class DumbMonster(PlayableObject):
    """An generic adversary.
    """
    tile="adversary"
    name="unspecified monster"
    appearance="featureless monster"
    vitality=5
    maxhp=5
    def initialise_playable(self):
        """Just been spawned.  Do what?"""
        self.inventory=Container(self.level)
        self.inventory.insert(GridObject(self.level))
        self.inventory.insert(GridObject(self.level))
        self.inventory.insert(GridObject(self.level))
        self.add_handler(1,self.onetick)
    def onetick(self):
        if self.interface!=None:
            return
        if self.vitality<=0:
            self.die()
            return
        type_=random.randrange(9)
        for i in range(1):
            if type_==0: target=(self.pt[0],self.pt[1]+1)
            if type_==1: target=(self.pt[0]+1,self.pt[1])
            if type_==2: target=(self.pt[0],self.pt[1]-1)
            if type_==3: target=(self.pt[0]-1,self.pt[1])
            if type_==4: target=(self.pt[0],self.pt[1])
            if type_==5: target=(self.pt[0]+1,self.pt[1]+1)
            if type_==6: target=(self.pt[0]-1,self.pt[1]-1)
            if type_==7: target=(self.pt[0]-1,self.pt[1]+1)
            if type_==8: target=(self.pt[0]+1,self.pt[1]-1)
            try: #XXX kludge/fragile/assumes
                floorlevel=type(0)(self.level.get_index_grid(*self.pt)[0][5:])
            except ValueError:
                floorlevel=1 #Needed or mazed subclass breaks
            nxtstat=self.level.get_index_grid(*target)[0]
            if self.level.objgrid[target[0]][target[1]]:
                breakp=1
                for obj in self.level.objgrid[target[0]][target[1]][:]:
                    if hasattr(obj,"interface") and obj.interface!=None:
                        if type(self) in obj.known:
                            obj.interface.backend.push_message("The %s hits!"%self.name)
                        else:
                            obj.interface.backend.push_message("The %s hits!"%self.appearance)
                        obj.vitality-=1
                        return
                else:
                    breakp=0
                if breakp:
                    break
            elif nxtstat.startswith("floor"):
                newlevel=type(0)(nxtstat[5:])
                if (newlevel-floorlevel)<=1:
                    break
            type_+=1
            type_%=4
        else: #i.e. ran to completion with no break
            return #stuck, cannot move
        self.place(*target)
        self.level.playerobj.interface.redraw()
