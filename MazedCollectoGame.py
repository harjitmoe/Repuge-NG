import sys,random,time
from repugeng.Level import Level
from repugeng.MazeLevel import MazeLevel
from repugeng.DumbFovLevel import DumbFovLevel
from repugeng.MultilevelStorage import MultilevelStorage
from BasicCollectoGame import BasicCollectoGame

NUMBERSIZE=8 #Cannot be bigger than 8


class MazedCollectoGame(BasicCollectoGame,MazeLevel):
    #More than one symbol per type can be defined: these
    # can then be distinguished in the run code
    list_of_symbols={"g":"wall_corner_nw","G":"wall_corner_ne","j":"wall_corner_sw","J":"wall_corner_se","d":"vwall","o":"hwall",":":"vfeature","*":"vfeature"," ":"space",".":"floor1",",":"floor2","/":"floor3","$":"floor4","#":"floor5","P":"hfeature","l":"hfeature","v":"wall_TeeJnc_dn","^":"wall_TeeJnc_up",">":"wall_TeeJnc_rt","<":"wall_TeeJnc_lt","+":"wall_cross",}
    title_window="Repuge-NG Collecto: Maze Edition"
    
    def get_new_point(self):
        if hasattr(self,"pt"):
            userloc=[self.pt]
        else:
            userloc=[self.starting_pt]
        while 1:
            x=random.randrange(1,NUMBERSIZE)*2+1 #Yes, *2)+1 OUTSIDE the brackets (and not *(2+1) which is *3)
            y=random.randrange(1,NUMBERSIZE)*2+1 #Yes, *2)+1 OUTSIDE the brackets (and not *(2+1) which is *3)
            if (x,y) not in self.beanpoints+userloc:
                return (x,y)
    
    def readmap(self):
        #Initialise scoring storage
        self.score=MultilevelStorage("collecto_score")
        self.score.myscore=0
        self.score.mymoves=0
        #Generate maze
        MazeLevel.readmap(self,NUMBERSIZE)
        #Put beans in unique locations
        self.beanpoints=[]
        for junk in range(NUMBERSIZE):#range must not be larger than NUMBERSIZE squared minus 1.  Final "bean" is actually the down staircase.
            self.beanpoints.append(self.get_new_point())
        for x,y in self.beanpoints[:-1]:
            self.objgrid[x][y]=("bean","'")
        x,y=self.beanpoints[-1]
        self.grid[x][y]=("ingredient","%") #I did not think the selections through well...
        #
        self.nan=0
    
    def handle_command(self,e):
        if e in (">","\r","\n","\r\n"," ","return","enter","space") and self.get_index_grid(*self.pt)[0]=="ingredient": #ie Staircase
            #Regen the dungeon.
            MazedCollectoGame()
#
if __name__=="__main__":
    l=MazedCollectoGame()
