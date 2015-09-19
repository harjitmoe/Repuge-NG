import time, sys, traceback
from repugeng.PlayerObject import PlayerObject
from repugeng.SimpleInterface import SimpleInterface
from repugeng.Compat3k import Compat3k

class Game(object):
    """ A game, comprising one or more levels.
    """
    #
    #Debugging settings, nothing to see here
    debug = 0
    bug_report = {}
    debug_ghost = 0
    debug_fov_off = 0
    #
    #For subclasses to override or not
    InterfaceClass = SimpleInterface
    PlayerClass = PlayerObject
    title_window = "Repuge-NG Application"
    use_rpc = False
    #
    def __init__(self):
        self.bug_report[__name__] = {}
        try:
            self.add_players()
            self.run()
        except SystemExit:
            raise
        except KeyboardInterrupt:
            raise
        except: #pylint: disable = bare-except
            exctype, exception, trace = sys.exc_info()
            try:
                #Put the exception in: the program quits on exception and,
                #unless started from a shell such as cmd, the terminal
                #probably closes promptly leaving it inaccessible.
                self.bug_report[__name__]["Exception"] = (exctype, exception,
                                                          traceback.extract_tb(trace))
                self.dump_report()
            except: #Keep squealing, pylint, this one needs work
                pass #Silence the irrelevant exception, making the above very hard to debug ;)
            if sys.hexversion < 0x03000000:
                #Only 2k way to keep original traceback here, exec'd as invalid 3k syntax
                exec("raise exctype, exception, trace") #pylint: disable = exec-used
            else:
                raise exception
    #
    def dump_report(self):
        import pickle
        f = open("bugreport.%010d.txt"%time.time(), "w")
        pickle.dump(self.bug_report, f)
        f.close()
    #
    def run(self):
        if self.use_rpc:
            print ("Please do not close this.") #pylint: disable = superfluous-parens
            import code
            code.interact(banner="Entering leader debug prompt...", local=locals())
        else:
            while 1:
                #Idle as subservient threads do the work
                time.sleep(10000)
    #
    loading_lock = 0
    def add_players(self):
        self.loading_lock = 1
        self._p = players = []
        if self.use_rpc:
            number = int(Compat3k.prompt_user("How many players (+ve number in figures): "))
            print ("Please start %d instance(s) " #pylint: disable = superfluous-parens
                   "of remote.py or remote.exe with unique ports."%number)
            print ("Once you have done this, " #pylint: disable = superfluous-parens
                   "enter the hosts and ports here.")
        else:
            number = 1
        for i in range(number):  #pylint: disable = unused-variable
            players.append(self.PlayerClass(self, play=1))
        for playerobj in players:
            self.level_initiate(playerobj)
        self.loading_lock = 0
    #
    def level_initiate(self, playerobj):
        raise NotImplementedError
    #
    def level_advance(self, playerobj):
        raise NotImplementedError
    #
    def level_regress(self, playerobj):
        raise NotImplementedError
