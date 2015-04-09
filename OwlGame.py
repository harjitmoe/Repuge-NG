import sys,random,time,math
from repugeng.Level import Level
from repugeng.MultilevelStorage import MultilevelStorage
from repugeng.GridObject import GridObject
from prelevula.RoomLevel import RoomLevel
from OwlObject import OwlObject

class OwlGame(RoomLevel):
    coded_grid=None #?
    title_window="Creature test"

    def get_new_point(self):
        if hasattr(self,"pt"):
            userloc=self.pt
        else:
            userloc=self.starting_pt
        while 1:
            (x,y)=random.choice(self.gamut)
            if (x,y) != userloc:
                return (x,y)

    def initmap(self):
        #Initialise scoring storage
        self.score=MultilevelStorage("owl_score")
        self.score.initialise_property("myscore",0)
        self.score.initialise_property("mymoves",0)
        #Generate map
        self.genmap()
        self.starting_pt=random.choice(self.gamut)
        #Place owl
        self.owl=OwlObject(self)
        x,y=self.get_new_point()
        self.owl.place(x,y)

    def handle_move(self,target):
        try: #XXX kludge/fragile/assumes
            floorlevel=type(0)(self.get_index_grid(*self.pt)[0][5:])
        except ValueError:
            floorlevel=1 #Needed or mazed subclass breaks
        nxtstat=self.get_index_grid(*target)[0]
        if self.objgrid[target[0]][target[1]]:
            for obj in self.objgrid[target[0]][target[1]][:]:
                pass
        elif nxtstat.startswith("floor"):
            newlevel=type(0)(nxtstat[5:])
            if (newlevel-floorlevel)<=1:
                if (newlevel-floorlevel)==1:
                    self.backend.push_message("You climb up")
                elif (newlevel-floorlevel)<0:
                    self.backend.push_message("You jump down")
                return 1
            else:
                self.backend.push_message("You try to climb but can't")
                return 0
        elif nxtstat=="staircase":
            self.backend.push_message("You find a staircase (use Return (enter) to descend).")
            return 1
        elif nxtstat=="space":
            self.backend.push_message("You hit the tunnel wall.")
            return 0
        else:
            self.backend.push_message("You hit something.")
            return 0
    
    def handle_command(self,e):
        if e in (">","\r","\n","\r\n"," ","return","enter","space") and self.get_index_grid(*self.pt)[0]=="staircase":
            #Regen the dungeon.
            CollectoGame.get_next_leveltype()() #yes, two ()
#
if __name__=="__main__":
    OwlGame()