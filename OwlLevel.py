import sys,random,time,math
from ludicrous.Level import Level
from ludicrous.MultilevelStorage import MultilevelStorage
from ludicrous.GridObject import GridObject
from ludicrous.DijkstraMonster import DijkstraMonster
from prelevula.RoomLevel import RoomLevel
from prelevula.MazeLevel2 import MazeLevel2
from OwlObject import OwlObject

class OwlLevel(MazeLevel2):
    coded_grid=None #?
    title_window="Creature test"
    use_dm=True
    def initmap(self):
        self.genmap(10,10)
        self.starting_pt=random.choice(self.gamut)

    def get_new_point(self):
        while 1:
            (x,y)=random.choice(self.gamut)
            if (x,y) != self.starting_pt:
                return (x,y)

    def initialise(self):
        #Place owl
        self.owl=OwlObject(self.game)
        x,y=self.get_new_point()
        self.owl.place(x,y,self)

    def handle_move(self,target,playerobj):
        try: #XXX kludge/fragile/assumes
            floorlevel=type(0)(self.get_index_grid(*playerobj.pt)[0][5:])
        except ValueError:
            floorlevel=1 #Needed or mazed subclass breaks
        nxtstat=self.get_index_grid(*target)[0]
        if self.objgrid[target[0]][target[1]]:
            for obj in self.objgrid[target[0]][target[1]][:]:
                if isinstance(obj,DijkstraMonster):
                    if type(obj) in playerobj.known:
                        playerobj.myinterface.push_message("You hit the %s!"%obj.name)
                    else:
                        playerobj.myinterface.push_message("You hit the %s!"%obj.appearance)
                    obj.vitality-=1
                    return 0
            playerobj.myinterface.push_message("There is something here.")
            return 1
        elif nxtstat.startswith("floor"):
            newlevel=type(0)(nxtstat[5:])
            if (newlevel-floorlevel)<=1:
                if (newlevel-floorlevel)==1:
                    playerobj.myinterface.push_message("You climb up")
                elif (newlevel-floorlevel)<0:
                    playerobj.myinterface.push_message("You jump down")
                return 1
            else:
                playerobj.myinterface.push_message("You try to climb but can't")
                return 0
        elif nxtstat=="staircase":
            playerobj.myinterface.push_message("You find a staircase (use Return (enter) to descend).")
            return 1
        elif nxtstat=="space":
            playerobj.myinterface.push_message("You hit the tunnel wall.")
            return 0
        else:
            playerobj.myinterface.push_message("You hit something.")
            return 0
    
    def handle_command(self,e,playerobj):
        if e in (">","\r","\n","\r\n"," ","return","enter","space") and self.get_index_grid(*playerobj.pt)[0]=="staircase":
            #Regen the dungeon.
            #CollectoGame.get_next_leveltype()() #yes, two ()
            pass
        elif e=="o":
            playerobj.polymorph(OwlObject)
        elif e=="i":
            return playerobj.report_inventory()
        elif e in ("t",):
            return playerobj.ask_throw()
        elif e in (",","#pickup"):
            return playerobj.ask_pickup()
        return 0
