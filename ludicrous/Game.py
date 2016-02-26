import sys, time
from ludicrous.PlayerObject import PlayerObject
from ludicrous.SimpleInterface import SimpleInterface
from consolation.Compat3k import Compat3k

__copying__="""
Written by Thomas Hori

This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/."""

class Game(object):
    """ A game, comprising one or more levels.
    """
    #
    #Debugging settings, nothing to see here
    debug = 0
    debug_ghost = 0
    debug_fov_off = 0
    #
    #For subclasses to override or not
    InterfaceClass = SimpleInterface
    PlayerClass = PlayerObject
    title_window = "Ludicrous Application"
    use_rpc = False
    #
    def __init__(self):
        self.add_players()
        self.run()
    #
    def run(self):
        if self.use_rpc:
            print ("Please do not close this.") #pylint: disable = superfluous-parens
            import code
            code.interact(banner="Entering leader debug prompt...", local=locals())
        else:
            while 1:
                try:
                    #Idle as subservient threads do the work
                    time.sleep(5)
                except KeyboardInterrupt:
                    for player in self._p:
                        player.myinterface.display.clean()
                    sys.exit()
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
