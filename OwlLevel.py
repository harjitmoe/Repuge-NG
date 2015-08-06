import sys,random,time,math
from repugeng.Level import Level
from repugeng.MultilevelStorage import MultilevelStorage
from repugeng.GridObject import GridObject
from repugeng.DumbMonster import DumbMonster
from prelevula.RoomLevel import RoomLevel
from prelevula.ExperimentalDungeonLevel import ExperimentalDungeonLevel
from OwlObject import OwlObject

class OwlLevel(ExperimentalDungeonLevel):
    coded_grid=None #?
    title_window="Creature test"

    def get_new_point(self):
        if hasattr(self,"pt"):
            userloc=self.playerobj.pt
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
        self.genmap()#10)
        self.starting_pt=random.choice(self.gamut)

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
                if isinstance(obj,DumbMonster):
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
        elif e in (",","#pickup"):
            for obj in self.objgrid[playerobj.pt[0]][playerobj.pt[1]][:]:
                if obj==playerobj:
                    continue
                while 1:
                    if type(obj) in playerobj.known:
                        ans=playerobj.myinterface.ask_question("Pick up a %s [ynq]? "%obj.name)
                    else:
                        ans=playerobj.myinterface.ask_question("Pick up a %s [ynq]? "%obj.appearance)
                    ans=ans.lower().strip()
                    if ans in "ynq":
                        break
                if ans=="y":
                    playerobj.inventory.insert(obj)
                elif ans=="n":
                    pass
                else: #ans=="q"
                    return
