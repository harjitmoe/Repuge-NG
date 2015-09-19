from repugeng.GridObject import GridObject
import random,time

class CollectoObject(GridObject):
    """An collectone.
    """
    tile="item"
    nan=65536
    name="collectone"
    appearance="floating spheroid"
    #
    def handle_contact(self,playerobj):
        self.level.redraw()
        duration=random.normalvariate(15,5)
        if duration<5:
            duration=5
        timr=time.time()
        result=self.question_test(duration,playerobj)
        if result!=-1:
            self.level.score.mymoves=self.level.score.mymoves+1
            timr=time.time()-timr
            if timr>duration:
                playerobj.myinterface.push_message("OVERTIME")
                result=False
            if result:
                if self.game.debug:
                    self.level.score.myscore=0
                    playerobj.myinterface.push_message("Debug mode is ON, nullifying score")
                else:
                    self.level.score.myscore+=int((100.0/timr)+0.5)
                    playerobj.myinterface.push_message(repr(self.level.score.myscore)+" total points, "+repr(self.level.score.mymoves)+" done, %.0f average points (point v10.1)"%(self.level.score.myscore/float(self.level.score.mymoves)))
            self.place(*self.level.get_new_point())
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
    def question_test(self,duration,playerobj):
        do_sum=random.randrange(2)
        do_arc=random.randrange(2)
        if do_sum:
            if not do_arc:
                n=random.randrange(100)
                m=random.randrange(100)
                ri=self.user_input_to_int(playerobj.myinterface.slow_ask_question(("in %.2f seconds, "%duration)+repr(n)+"+"+repr(m)+"="))
                if ri!=ri: #i.e. is NaN
                    playerobj.myinterface.push_message("I don't understand that answer (in figures, please).")
                    return -1
                elif ri!=n+m:
                    playerobj.myinterface.push_message("wrong, it's "+str(n+m))
                    return False
                else:
                    playerobj.myinterface.push_message("right")
                    return True
            else:
                #Note: ALL PRE-NG COLLECTO VERSIONS had a 1/400 chance of failing 
                #on each try with "empty range for randrange()".  This is fixed in
                #this NG version.
                n=random.randrange(1,100)
                m=random.randrange(n)
                ri=self.user_input_to_int(playerobj.myinterface.slow_ask_question(("in %.2f seconds, "%duration)+repr(n)+"-"+repr(m)+"="))
                if ri!=ri: #i.e. is NaN
                    playerobj.myinterface.push_message("I don't understand that answer (in figures, please).")
                    return -1
                elif ri!=n-m:
                    playerobj.myinterface.push_message("wrong, it's "+str(n-m))
                    return False
                else:
                    playerobj.myinterface.push_message("right")
                    return True
        else:
            if not do_arc:
                n=random.randrange(1,10)
                m=random.randrange(1,10)
                ri=self.user_input_to_int(playerobj.myinterface.slow_ask_question(("in %.2f seconds, "%duration)+repr(n)+" times "+repr(m)+"="))
                if ri!=ri: #i.e. is NaN
                    playerobj.myinterface.push_message("I don't understand that answer (in figures, please).")
                    return -1
                elif ri!=n*m:
                    playerobj.myinterface.push_message("wrong, it's "+str(n*m))
                    return False
                else:
                    playerobj.myinterface.push_message("right")
                    return True
            else:
                #Integer division!  NOTE: DO NOT ADD FLOAT DIVISION.  
                #UNREASONABLE TO COMPARE FLOATS.  LOOKUP WHY.
                #Hint: try evaluating sum([0.0001]*50000)==5
                #See also the "decimal" module.
                n=random.randrange(20)
                m=random.randrange(1,5)
                n*=m
                ri=self.user_input_to_int(playerobj.myinterface.slow_ask_question(("in %.2f seconds, "%duration)+repr(n)+" divided by "+repr(m)+"="))
                if ri!=ri: #i.e. is NaN
                    playerobj.myinterface.push_message("I don't understand that answer (in figures, please).")
                    return -1
                elif ri!=n//m: #Integer division!
                    playerobj.myinterface.push_message("wrong, it's "+str(n//m)) #Integer division!
                    return False
                else:
                    playerobj.myinterface.push_message("right")
                    return True
