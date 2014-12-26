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
import sys,random,time
from repugeng.Level import Level
from repugeng.MultilevelStorage import MultilevelStorage

NUMBERSIZE=15 #Cannot be bigger than 17

class BasicCollectoGame(Level):
    coded_grid=None
    #More than one symbol per type can be defined: these
    # can then be distinguished in the run code
    list_of_symbols={"g":"wall_corner_nw","G":"wall_corner_ne","j":"wall_corner_sw","J":"wall_corner_se","d":"vwall","o":"hwall",":":"vfeature","*":"vfeature"," ":"space",".":"floor1",",":"floor2","/":"floor3","$":"floor4","#":"floor5","P":"hfeature","l":"hfeature"}
    title_window="Repuge-NG Collecto: Basic Edition"
    starting_pt=(1,1)
    
    def readmap(self):
        #Initialise scoring storage
        self.score=MultilevelStorage("collecto_score")
        self.score.initialise_property("myscore",0)
        self.score.initialise_property("mymoves",0)
        #Generate base grid
        self.coded_grid="g"+("o"*NUMBERSIZE)+"G\n"+("d"+("."*NUMBERSIZE)+"d\n")*NUMBERSIZE+"j"+("o"*NUMBERSIZE)+"J"
        super(BasicCollectoGame,self).readmap()
        #Put beans in unique locations
        beanpoints=[]
        blockpoints=[]
        for junk in range(NUMBERSIZE):#ranges total must not be larger than NUMBERSIZE squared minus 1.
            while 1:
                x=random.randrange(1,NUMBERSIZE)
                y=random.randrange(1,NUMBERSIZE)
                if (x,y) not in beanpoints+blockpoints:
                    beanpoints.append((x,y))
                    break
        #ranges total must not be larger than NUMBERSIZE squared.
        for junk in range(1):#this range must not be larger than 2 (or 1 if no numberpad-with-numlock-on)
            while 1:
                x=random.randrange(1,NUMBERSIZE)
                y=random.randrange(1,NUMBERSIZE)
                if (x,y) not in beanpoints+blockpoints:
                    blockpoints.append((x,y))
                    break
        for x,y in beanpoints:
            self.objgrid[x][y]=("bean","'")
        for x,y in blockpoints:
            self.grid[x][y]=("boulder","O")
        #
        self.nan=0
    def handle_move(self,target):
        floorlevel=type(0)(self.get_index_grid(*self.pt)[0][5:]) #XXX kludge/fragile/assumes
        curstat=self.get_index_grid(*self.pt)[0]
        nxtstat=self.get_index_grid(*target)[0]
        if self.get_index_objgrid(*target):
            if self.get_index_objgrid(*target)[0]=="bean":
                duration=5+random.expovariate(0.2)
                timr=time.time()
                result=self.question_test(duration)
                self.score.mymoves=self.score.mymoves+1
                timr=time.time()-timr
                if timr>duration:
                    self.backend.push_message("OVERTIME")
                    result=False
                if result:
                    self.score.myscore+=int((100.0/timr)+0.5)
                    self.backend.push_message(repr(self.score.myscore)+" total points, "+repr(self.score.mymoves)+" done, %.0f average points (point v2)"%(self.score.myscore/float(self.score.mymoves)))
                self.set_index_objgrid((),*target)
                while 1:
                    #New location where there is not already something
                    x=random.randrange(1,NUMBERSIZE)
                    y=random.randrange(1,NUMBERSIZE)
                    if not self.objgrid[x][y]:
                        self.objgrid[x][y]=("bean","'")
                        break
            return 0
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
        elif nxtstat=="ingredient": #ie Staircase
            self.backend.push_message("You find a staircase (use Return (enter) to descend).")
            return 1
        elif nxtstat=="space":
            self.backend.push_message("You decide not to jump into the abyss")
            return 0
        else:
            self.backend.push_message("You hit something")
            return 0
    #
    def user_input_to_int(self,input,base=10):
        try:
            return int(input,base)
        except ValueError:
            self.backend.push_message("Wrong!  Hint: it's a number in figures.")
            exp="1e+1"
            #json.decode("nan") would work were I aiming at 2.7 only.
            while self.nan==self.nan:
                exp+="0"
                #Sign bit would seem to distinguish between "indeterminable"
                #and "quiet not-a-number".  Eh?  How many NaNs does one need?
                self.nan=-(float(exp)/float(exp))
            return self.nan
    #
    def question_test(self,duration):
        do_sum=random.randrange(2)
        do_arc=random.randrange(2)
        if do_sum:
            if not do_arc:
                n=random.randrange(100)
                m=random.randrange(100)
                ri=self.backend.slow_ask_question(("in %.2f seconds, "%duration)+repr(n)+"+"+repr(m)+"=")
                if self.user_input_to_int(ri)!=n+m:
                    self.backend.push_message("wrong, it's "+str(n+m))
                    return False
                else:
                    self.backend.push_message("right")
                    return True
            else:
                #Note: ALL PRE-NG COLLECTO VERSIONS had a 1/400 chance of failing 
                #on each try with "empty range for randrange()".  This is fixed in
                #this NG version.
                n=random.randrange(1,100)
                m=random.randrange(n)
                ri=self.backend.slow_ask_question(("in %.2f seconds, "%duration)+repr(n)+"-"+repr(m)+"=")
                if self.user_input_to_int(ri)!=n-m:
                    self.backend.push_message("wrong, it's "+str(n-m))
                    return False
                else:
                    self.backend.push_message("right")
                    return True
        else:
            if not do_arc:
                n=random.randrange(1,10)
                m=random.randrange(1,10)
                ri=self.backend.slow_ask_question(("in %.2f seconds, "%duration)+repr(n)+" times "+repr(m)+"=")
                if self.user_input_to_int(ri)!=n*m:
                    self.backend.push_message("wrong, it's "+str(n*m))
                    return False
                else:
                    self.backend.push_message("right")
                    return True
            else:
                #Integer division!  NOTE: DO NOT ADD FLOAT DIVISION.  UNREASONABLE TO COMPARE FLOATS.  LOOKUP WHY.  See also the "decimal" module.
                n=random.randrange(20)
                m=random.randrange(1,5)
                n*=m
                ri=self.backend.slow_ask_question(("in %.2f seconds, "%duration)+repr(n)+" divided by "+repr(m)+"=")
                if self.user_input_to_int(ri)!=n//m: #Integer division!
                    self.backend.push_message("wrong, it's "+str(n//m)) #Integer division!
                    return False
                else:
                    self.backend.push_message("right")
                    return True
#
if __name__=="__main__":
    BasicCollectoGame()
