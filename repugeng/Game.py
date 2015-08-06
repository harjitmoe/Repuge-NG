import time,sys,traceback
from repugeng.GridObject import GridObject
from repugeng.PlayableObject import PlayableObject
from repugeng.SimpleInterface import SimpleInterface
from repugeng.Level import Level

class Game(object):
    #
    #Debugging settings, nothing to see here
    debug=0
    bug_report={}
    debug_ghost=0
    debug_fov_off=0
    #
    #For subclasses to override or not
    InterfaceClass=SimpleInterface
    PlayerClass=PlayableObject
    title_window="Repuge-NG Application"
    use_rpc=False
    #
    def __init__(self,start=1):
        self.bug_report[__name__]={}
        try:
            self.interfaces=[]
            self.add_players()
            self.run()
        except SystemExit:
            raise
        except KeyboardInterrupt:
            raise
        except:
            exctype,exception,trace=sys.exc_info()
            try:
                #Put the exception in: the program quits on exception and, 
                #unless started from a shell such as cmd, the terminal 
                #probably closes promptly leaving it inaccessible.
                self.bug_report[__name__]["Exception"]=(exctype,exception,traceback.extract_tb(trace))
                self.bug_report[__name__]["grid"]=self.grid
                self.bug_report[__name__]["objgrid"]=self.objgrid
                self._dump_report()
            except:
                pass #Silence the irrelevant exception
            if sys.hexversion<0x03000000:
                #Only 2k way to keep original traceback here, exec'd as invalid 3k syntax
                exec("raise exctype,exception,trace")
            else:
                raise exception
    #
    def run(self):
        while 1:
            #Each creature gets a move:
            for obj in GridObject.all_objects:
                obj.tick()
    #
    interfaces=None
    def redraw(self):
        for aninterface in self.interfaces:
            aninterface.redraw()
    #
    def add_players(self):
        if self.use_rpc:
            number=int(raw_input("How many players (+ve number in figures): "))
            print ("Please start %d instance(s) of remote.py with unique ports."%number)
            print ("Once you have done this, enter the port numbers here.")
        else:
            number=1
        for i in range(number):
            playerobj=self.PlayerClass(self,play=1)
            self.level_initiate(playerobj)
    #
    def level_initiate(self,playerobj):
        raise NotImplementedError
    #
    def level_advance(self,playerobj):
        raise NotImplementedError
    #
    def level_regress(self,playerobj):
        raise NotImplementedError
