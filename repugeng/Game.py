import time,sys,traceback
from repugeng.GridObject import GridObject
from repugeng.PlayableObject import PlayableObject
from repugeng.SimpleInterface import SimpleInterface
from repugeng.Level import Level

class Game(object):
    #Debugging settings, nothing to see here
    debug=0
    bug_report={}
    debug_ghost=0
    debug_fov_off=0
    #
    InterfaceClass=SimpleInterface
    PlayerClass=PlayableObject
    title_window="Repuge-NG Application"
    #
    playerobj=None
    level=None
    #
    def __init__(self,start=1):
        self.bug_report[__name__]={}
        try:
            self.playerobj=self.PlayerClass(self,play=1)
            self.level=self.gen_next_level()
            self.level.game=self
            self.level.boot(start)
        except SystemExit:
            raise
        except:
            exctype,exception,traceback=sys.exc_info()
            try:
                #Put the exception in: the program quits on exception and, 
                #unless started from a shell such as cmd, the terminal 
                #probably closes promptly leaving it inaccessible.
                self.bug_report[__name__]["Exception"]=(exctype,exception,traceback.extract_tb(traceback))
                self.bug_report[__name__]["grid"]=self.grid
                self.bug_report[__name__]["objgrid"]=self.objgrid
                self._dump_report()
            except:
                pass #Silence the irrelevant exception
            if sys.hexversion<0x03000000:
                #Only 2k way to keep original traceback here, exec'd as invalid 3k syntax
                exec("raise exctype,exception,traceback")
            else:
                raise exception
    #
    def gen_next_level(self):
        """Returns a level object.  Called to generate a new level."""
        raise NotImplementedError
    
