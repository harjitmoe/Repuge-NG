from repugeng.GridObject import GridObject
from repugeng.PlayerObject import PlayerObject
import random,time

class CollectoObject(GridObject):
    """An collectone.
    """
    tile="item"
    nan=65536
    def tick(self):
        if self.nan==self.nan and hasattr(self.level,"nan"):
            self.nan=self.level.nan
        for i in range(5):
            type_=random.randrange(5)
            if type_==0: target=(self.pt[0],self.pt[1]+1)
            if type_==1: target=(self.pt[0]+1,self.pt[1])
            if type_==2: target=(self.pt[0],self.pt[1]-1)
            if type_==3: target=(self.pt[0]-1,self.pt[1])
            if type_==4: target=(self.pt[0],self.pt[1])
            try: #XXX kludge/fragile/assumes
                floorlevel=type(0)(self.level.get_index_grid(*self.pt)[0][5:])
            except ValueError:
                floorlevel=1 #Needed or mazed subclass breaks
            nxtstat=self.level.get_index_grid(*target)[0]
            if self.level.objgrid[target[0]][target[1]]:
                breakp=1
                for obj in self.level.objgrid[target[0]][target[1]][:]:
                    if isinstance(obj,PlayerObject):
                        self.handle_contact()
                else:
                    breakp=0
                if breakp:
                    break
            elif nxtstat.startswith("floor"):
                newlevel=type(0)(nxtstat[5:])
                if (newlevel-floorlevel)<=1:
                    break
            type_+=1
            type_%=5
        else: #i.e. ran to completion with no break
            return #stuck, cannot move
        self.place(*target)
    #
    def handle_contact(self):
        self.level.bug_report[__name__]={}
        duration=random.normalvariate(15,5)
        self.level.bug_report[__name__]["duration"]=duration
        if duration<5:
            duration=5
        timr=time.time()
        result=self.question_test(duration)
        self.level.bug_report[__name__]["result"]=result
        if result!=-1:
            self.level.score.mymoves=self.level.score.mymoves+1
            timr=time.time()-timr
            if timr>duration:
                self.level.playerobj.interface.backend.push_message("OVERTIME")
                result=False
            if result:
                if self.level.debug:
                    self.level.score.myscore=0
                    self.level.playerobj.interface.backend.push_message("Debug mode is ON, nullifying score")
                else:
                    self.level.score.myscore+=int((100.0/timr)+0.5)
                    self.level.playerobj.interface.backend.push_message(repr(self.level.score.myscore)+" total points, "+repr(self.level.score.mymoves)+" done, %.0f average points (point v10.1)"%(self.level.score.myscore/float(self.level.score.mymoves)))
            self.place(*self.level.get_new_point())
    #
    def user_input_to_int(self,input):
        self.level.bug_report[__name__]["input"]=input
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
        self.level.bug_report[__name__]["do_sum"]=do_sum
        self.level.bug_report[__name__]["do_arc"]=do_arc
        if do_sum:
            if not do_arc:
                n=random.randrange(100)
                m=random.randrange(100)
                ri=self.user_input_to_int(self.level.playerobj.interface.backend.slow_ask_question(("in %.2f seconds, "%duration)+repr(n)+"+"+repr(m)+"="))
                if ri!=ri: #i.e. is NaN
                    self.level.playerobj.interface.backend.push_message("I don't understand that answer (in figures, please).")
                    return -1
                elif ri!=n+m:
                    self.level.playerobj.interface.backend.push_message("wrong, it's "+str(n+m))
                    return False
                else:
                    self.level.playerobj.interface.backend.push_message("right")
                    return True
            else:
                #Note: ALL PRE-NG COLLECTO VERSIONS had a 1/400 chance of failing 
                #on each try with "empty range for randrange()".  This is fixed in
                #this NG version.
                n=random.randrange(1,100)
                m=random.randrange(n)
                ri=self.user_input_to_int(self.level.playerobj.interface.backend.slow_ask_question(("in %.2f seconds, "%duration)+repr(n)+"-"+repr(m)+"="))
                if ri!=ri: #i.e. is NaN
                    self.level.playerobj.interface.backend.push_message("I don't understand that answer (in figures, please).")
                    return -1
                elif ri!=n-m:
                    self.level.playerobj.interface.backend.push_message("wrong, it's "+str(n-m))
                    return False
                else:
                    self.level.playerobj.interface.backend.push_message("right")
                    return True
        else:
            if not do_arc:
                n=random.randrange(1,10)
                m=random.randrange(1,10)
                ri=self.user_input_to_int(self.level.playerobj.interface.backend.slow_ask_question(("in %.2f seconds, "%duration)+repr(n)+" times "+repr(m)+"="))
                if ri!=ri: #i.e. is NaN
                    self.level.playerobj.interface.backend.push_message("I don't understand that answer (in figures, please).")
                    return -1
                elif ri!=n*m:
                    self.level.playerobj.interface.backend.push_message("wrong, it's "+str(n*m))
                    return False
                else:
                    self.level.playerobj.interface.backend.push_message("right")
                    return True
            else:
                #Integer division!  NOTE: DO NOT ADD FLOAT DIVISION.  
                #UNREASONABLE TO COMPARE FLOATS.  LOOKUP WHY.
                #Hint: try evaluating sum([0.0001]*50000)==5
                #See also the "decimal" module.
                n=random.randrange(20)
                m=random.randrange(1,5)
                n*=m
                ri=self.user_input_to_int(self.level.playerobj.interface.backend.slow_ask_question(("in %.2f seconds, "%duration)+repr(n)+" divided by "+repr(m)+"="))
                if ri!=ri: #i.e. is NaN
                    self.level.playerobj.interface.backend.push_message("I don't understand that answer (in figures, please).")
                    return -1
                elif ri!=n//m: #Integer division!
                    self.level.playerobj.interface.backend.push_message("wrong, it's "+str(n//m)) #Integer division!
                    return False
                else:
                    self.level.playerobj.interface.backend.push_message("right")
                    return True
