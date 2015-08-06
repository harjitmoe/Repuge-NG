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
            self.whence="starting"
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
    class AdvanceLevelException(BaseException):pass
    class RegressLevelException(BaseException):pass
    whence=None #starting, advancement, regression, jumping
    def run(self):
        #Designed to avoid gaining recursion levels with each level
        #Levels are advanced or regressed by exception control
        #Level.run is always executed at same stack depth
        while 1:
            try:
                self.level.bring_to_front(self.playerobj,self.whence)
                self.level.run()
            except Game.AdvanceLevelException:
                self.whence="advancement"
                self.level_advance()
            except Game.RegressLevelException:
                self.whence="regression"
                self.level_regress()
    #
    def level_advance(self):
        """Should set self.level and not be called directly.
        
        Please raise Game.AdvanceLevelException to trigger this."""
        raise NotImplementedError
    #
    def level_regress(self):
        """Should set self.level and not be called directly.
        
        Please raise Game.RegressLevelException to trigger this."""
        raise NotImplementedError
