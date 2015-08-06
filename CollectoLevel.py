"""Initial proposal (***note that this is not entirely followed*** (yet)):

- There is a universe, the player has to run around the universe (bird's-eye-view) collecting objects, which are inserted at random. A certain undecided number of objects are in the initial universe. 

- They will then be asked a random addition, subtraction, multiplication and division, the trickiness depending on the value of the object. 

- They will also be time-limited, with the more valuable objects having shorter time limits. 

- If they succeed, their score will be increased by the value of the object and it will vanish and another object will appear somewhere random, keeping the object count constant. 

- If they time out their score will stay the same, the object will not vanish and they will be able to pick it up again but the question will be different. 

- If they get it wrong, their score will be decreased by a certain undecided fraction of the object's value, it will vanish and another object will appear in a random location. 

- This is intended to help people practise their mental mathematics, and thus improve one's mathematical speed and ability. 

- This is aimed at people revising for SATs, GCSEs, A-levels... I will probably have to pick one (GCSE probably as it may be useful to me as well as others) but if I can find the time I might add multiple levels.
"""
import sys,random,math
from repugeng.Level import Level
from repugeng.MultilevelStorage import MultilevelStorage
from repugeng.GridObject import GridObject
from repugeng.SimpleInterface import SimpleInterface
from CollectoObject import CollectoObject

class CollectoLevel(Level):
    coded_grid=None
    title_window="Repuge-NG Collecto"

    def get_new_point(self):
        return random.choice(self.gamut)

    def initmap(self):
        #Initialise scoring storage
        self.score=MultilevelStorage("collecto_score")
        self.score.initialise_property("myscore",0)
        self.score.initialise_property("mymoves",0)
        #Generate map
        self.genmap()
        self.starting_pt=self.get_new_point()
        #Put collectones in unique locations
        for junk in range(int(math.sqrt(len(self.gamut)))):
            CollectoObject(self.game).place(*self.get_new_point()+(self,))
        x,y=self.get_new_point()
        self.grid[x][y]=("staircase","%")
        #
        self.nan=0
        self.children=[]
        #self.playerobj.myinterface.push_message("Use #quit to quit.")

    def handle_move(self,target,playerobj):
        try: #XXX kludge/fragile/assumes
            floorlevel=type(0)(self.get_index_grid(*playerobj.pt)[0][5:])
        except ValueError:
            floorlevel=1 #Needed or mazed subclass breaks
        nxtstat=self.get_index_grid(*target)[0]
        if self.objgrid[target[0]][target[1]]:
            for obj in self.objgrid[target[0]][target[1]][:]:
                if isinstance(obj,CollectoObject):
                    obj.handle_contact()
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
            raise self.game.AdvanceLevelException
        elif e=="#quit":
            sys.exit()
