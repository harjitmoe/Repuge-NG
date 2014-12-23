import sys,random,time
from Level import Level
from MultilevelStorage import MultilevelStorage

NUMBERSIZE=15 #Cannot be bigger than 17

class BasicCollectoGame(Level):
    coded_grid=None
    #More than one symbol per type can be defined: these
    # can then be distinguished in the run code
    list_of_symbols={"g":"wall_corner_nw","G":"wall_corner_ne","j":"wall_corner_sw","J":"wall_corner_se","d":"vwall","o":"hwall",":":"vfeature","*":"vfeature"," ":"space",".":"floor1",",":"floor2","/":"floor3","$":"floor4","#":"floor5","P":"hfeature","l":"hfeature"}
    title_window="Repuge Collecto"
    
    def readmap(self):
        self.coded_grid="g"+("o"*NUMBERSIZE)+"G\n"+("d"+("."*NUMBERSIZE)+"d\n")*NUMBERSIZE+"j"+("o"*NUMBERSIZE)+"J"
        super(BasicCollectoGame,self).readmap()
    def run(self):
        self.score=MultilevelStorage("collecto_score")
        try:
            self.backend.set_window_title(self.title_window)
        except NotImplementedError:
            pass
        myscore=0
        mymoves=0
        f=open("log.txt","w")
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
        #end
        pt=(1,1)
        self.move_user(pt,pt)
        while 1:
            self.redraw()
            e=self.backend.get_key_event()
            if e in ("\x03","\x04","\x1a"): #ETX ^C, EOT ^D, and ^Z
                #Does not go through to Python otherwise, meaning that Linux main terminals
                #are rendered otherwise out of order until someone kills Collecto
                #from a different terminal or over SSH (or rlogin).
                #This is relevent if someone is running this on an RPi.
                raise KeyboardInterrupt #^c, ^d or ^z pressed
            elif e in ("down","up","left","right","8","4","6","2"):
                if e in ("down","2"): targit=(pt[0],pt[1]+1)
                if e in ("right","6"):targit=(pt[0]+1,pt[1])
                if e in ("up","8"):   targit=(pt[0],pt[1]-1)
                if e in ("left","4"): targit=(pt[0]-1,pt[1])
                floorlevel=type(0)(self.get_index_grid(*pt)[0][5:]) #XXX kludge/fragile/assumes
                curstat=self.get_index_grid(*pt)[0]
                nxtstat=self.get_index_grid(*targit)[0]
                if self.get_index_objgrid(*targit):
                    if self.get_index_objgrid(*targit)[0]=="bean":
                        duration=5+random.expovariate(0.2)
                        timr=time.time()
                        result=self.question_test(duration)
                        mymoves=mymoves+1
                        timr=time.time()-timr
                        if timr>duration:
                            self.backend.push_message("OVERTIME")
                            result=False
                        if result:
                            myscore+=int((100.0/timr)+0.5)
                            self.backend.push_message(repr(myscore)+" total points, "+repr(mymoves)+" done, %.0f average points (point v2)"%(myscore/float(mymoves)))
                        self.set_index_objgrid((),*targit)
                        while 1:
                            #New location where there is not already something
                            x=random.randrange(1,NUMBERSIZE)
                            y=random.randrange(1,NUMBERSIZE)
                            if not self.objgrid[x][y]:
                                self.objgrid[x][y]=("bean","'")
                                break
                elif nxtstat.startswith("floor"):
                    newlevel=type(0)(nxtstat[5:])
                    if (newlevel-floorlevel)<=1:
                        if (newlevel-floorlevel)==1:
                            self.backend.push_message("You climb up")
                        elif (newlevel-floorlevel)<0:
                            self.backend.push_message("You jump down")
                        self.set_index_objgrid((),*pt)
                        pt=targit
                        self.set_index_objgrid(("user",None),*pt)
                        self.backend.goto_point(*pt)
                    else:
                        self.backend.push_message("You try to climb but can't")
                elif nxtstat=="ingredient": #ie Staircase
                    self.set_index_objgrid((),*pt)
                    pt=targit
                    self.set_index_objgrid(("user",None),*pt)
                    backend.gotopt(*pt)
                    self.backend.push_message("You find a staircase (use Return (enter) to decend).")
                    #readmap.ENABLE_SHADOWTRACING=0 #View from the stairs?
                elif nxtstat=="space":
                    self.backend.push_message("You decide not to jump into the abyss")
                else:
                    self.backend.push_message("You hit something")
    #
    def user_input_to_int(self,input,base=10,int=int):
        try:
            return int(input,base)
        except ValueError:
            self.backend.push_message("Wrong!  Hint: it's a number in figures.")
            global _nan #Therefore only calc it once (while loop...)
            exp="1e+1"
            while _nan==_nan:
                exp+="0"
                #Sign bit would seem to distinguish between "indeterminable"
                #and "quiet not-a-number".  Eh?  How many NaNs does one need?
                _nan=-(float(exp)/float(exp))
            return _nan
    #
    def question_test(self,duration):
        do_sum=random.randrange(2)
        do_arc=random.randrange(2)
        if do_sum:
            if not do_arc:
                n=random.randrange(100)
                m=random.randrange(100)
                ri=self.backend.slow_ask_question(("in %.2f seconds, "%duration)+repr(n)+"+"+repr(m)+"=")
                if int(ri)!=n+m:
                    self.backend.push_message("wrong, it's "+str(n+m))
                    return False
                else:
                    self.backend.push_message("right")
                    return True
            else:
                #Note: ALL PRE-NG COLLECTO VERSIONS had a 1/400 chance of failing 
                #on each try with "empty range for randrange()"
                n=random.randrange(1,100)
                m=random.randrange(n)
                ri=self.backend.slow_ask_question(("in %.2f seconds, "%duration)+repr(n)+"-"+repr(m)+"=")
                if int(ri)!=n-m:
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
                if int(ri)!=n*m:
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
                if int(ri)!=n//m: #Integer division!
                    self.backend.push_message("wrong, it's "+str(n//m)) #Integer division!
                    return False
                else:
                    self.backend.push_message("right")
                    return True
#
if __name__=="__main__":
    BasicCollectoGame()
