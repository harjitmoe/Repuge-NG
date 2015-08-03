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
    class AdvanceLevelException(BaseException):pass
    class RegressLevelException(BaseException):pass
    #
    title_window="Repuge-NG Application"
    #
    playerobj=None
    level=None
    #
    def __init__(self,start=1):
        self.bug_report[__name__]={}
        try:
            self.playerobj=self.PlayerClass(self,play=1)
            self.level_advance()
            self.run()
        except SystemExit:
            raise
        except KeyboardInterrupt:
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
    def run(self):
        #Designed to avoid gaining recursion levels with each level
        #Levels are advanced or regressed by exception control
        #Level.run is always executed at same stack depth
        while 1:
            try:
                self.level.run()
            except Game.AdvanceLevelException:
                self.level_advance()
            except Game.RegressLevelException:
                self.level_regress()
    #
    def level_advance(self):
        """Should set self.level"""
        raise NotImplementedError
    #
    def level_regress(self):
        """Should set self.level"""
        raise NotImplementedError
