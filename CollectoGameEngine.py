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
import sys,random,time,math
from repugeng.Level import Level
from repugeng.MultilevelStorage import MultilevelStorage

class CollectoGameEngine(Level):
    coded_grid=None
    title_window="Repuge-NG Collecto: Basic Edition"
    _leveltypes=[]
    
    @classmethod
    def register_leveltype(cls,subcls):
        cls._leveltypes.append(subcls)
    @classmethod
    def get_next_leveltype(cls):
        return random.choice(cls._leveltypes)

    def get_new_point(self):
        if hasattr(self,"pt"):
            userloc=[self.pt]
        else:
            userloc=[self.starting_pt]
        while 1:
            (x,y)=random.choice(self.gamut)
            if (x,y) not in self.beanpoints+userloc:
                return (x,y)

    def initmap(self):
        #Initialise scoring storage
        self.score=MultilevelStorage("collecto_score")
        self.score.initialise_property("myscore",0)
        self.score.initialise_property("mymoves",0)
        #Generate map
        self.genmap()
        self.starting_pt=random.choice(self.gamut)
        #Put beans in unique locations
        self.beanpoints=[]
        for junk in range(int(math.sqrt(len(self.gamut)))):
            self.beanpoints.append(self.get_new_point())
        for x,y in self.beanpoints[:-1]:
            self.objgrid[x][y]=("bean","'")
        x,y=self.beanpoints[-1]
        self.grid[x][y]=("ingredient","%") #I did not think the selections through well...
        #
        self.nan=0

    def handle_move(self,target):
        try: #XXX kludge/fragile/assumes
            floorlevel=type(0)(self.get_index_grid(*self.pt)[0][5:])
        except ValueError:
            floorlevel=1 #Needed or mazed subclass breaks
        curstat=self.get_index_grid(*self.pt)[0]
        nxtstat=self.get_index_grid(*target)[0]
        if self.get_index_objgrid(*target):
            if self.get_index_objgrid(*target)[0]=="bean":
                duration=random.normalvariate(15,5)
                if duration<5:
                    duration=5
                timr=time.time()
                result=self.question_test(duration)
                if result!=-1:
                    self.score.mymoves=self.score.mymoves+1
                    timr=time.time()-timr
                    if timr>duration:
                        self.backend.push_message("OVERTIME")
                        result=False
                    if result:
                        self.score.myscore+=int((100.0/timr)+0.5)
                        self.backend.push_message(repr(self.score.myscore)+" total points, "+repr(self.score.mymoves)+" done, %.0f average points (point v10.1)"%(self.score.myscore/float(self.score.mymoves)))
                    self.set_index_objgrid((),*target)
                    self.beanpoints.remove(target)
                    new_location=self.get_new_point()
                    self.beanpoints.append(new_location)
                    self.set_index_objgrid(("bean","'"),*new_location)
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
    def user_input_to_int(self,input):
        try:
            return int(input)
        except ValueError:
            try:
                flt=float(input)
                #Float comparison (never compare floats directly, see below)
                if abs(float(int(flt))-flt)<0.0001:
                    return int(flt)
                else: #Not equal, so further float comparison not an issue
                    return flt
            except ValueError:
                exp="1e+1"
                #json.decode("nan") would work were I aiming at 2.7+ only.
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
                ri=self.user_input_to_int(self.backend.slow_ask_question(("in %.2f seconds, "%duration)+repr(n)+"+"+repr(m)+"="))
                if ri!=ri: #i.e. is NaN
                    self.backend.push_message("I don't understand that answer (in figures, please).")
                    return -1
                elif ri!=n+m:
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
                ri=self.user_input_to_int(self.backend.slow_ask_question(("in %.2f seconds, "%duration)+repr(n)+"-"+repr(m)+"="))
                if ri!=ri: #i.e. is NaN
                    self.backend.push_message("I don't understand that answer (in figures, please).")
                    return -1
                elif ri!=n-m:
                    self.backend.push_message("wrong, it's "+str(n-m))
                    return False
                else:
                    self.backend.push_message("right")
                    return True
        else:
            if not do_arc:
                n=random.randrange(1,10)
                m=random.randrange(1,10)
                ri=self.user_input_to_int(self.backend.slow_ask_question(("in %.2f seconds, "%duration)+repr(n)+" times "+repr(m)+"="))
                if ri!=ri: #i.e. is NaN
                    self.backend.push_message("I don't understand that answer (in figures, please).")
                    return -1
                elif ri!=n*m:
                    self.backend.push_message("wrong, it's "+str(n*m))
                    return False
                else:
                    self.backend.push_message("right")
                    return True
            else:
                #Integer division!  NOTE: DO NOT ADD FLOAT DIVISION.  
                #UNREASONABLE TO COMPARE FLOATS.  LOOKUP WHY.
                #Hint: try evaluating sum([0.0001]*50000)==5
                #See also the "decimal" module.
                n=random.randrange(20)
                m=random.randrange(1,5)
                n*=m
                ri=self.user_input_to_int(self.backend.slow_ask_question(("in %.2f seconds, "%duration)+repr(n)+" divided by "+repr(m)+"="))
                if ri!=ri: #i.e. is NaN
                    self.backend.push_message("I don't understand that answer (in figures, please).")
                    return -1
                elif ri!=n//m: #Integer division!
                    self.backend.push_message("wrong, it's "+str(n//m)) #Integer division!
                    return False
                else:
                    self.backend.push_message("right")
                    return True
    
    def handle_command(self,e):
        if e in (">","\r","\n","\r\n"," ","return","enter","space") and self.get_index_grid(*self.pt)[0]=="ingredient": #ie Staircase
            #Regen the dungeon.
            CollectoGameEngine.get_next_leveltype()() #yes, two ()
#
if __name__=="__main__":
    import sys
    sys.modules["CollectoGameEngine"]=sys.modules["__main__"] #oh, Python
    import BasicCollectoGame,MazedCollectoGame,DungeonCollectoGame
    CollectoGameEngine.get_next_leveltype()() #yes, two ()

