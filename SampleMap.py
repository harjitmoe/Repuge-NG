#!/usr/bin/env python
from ludicrous.Level import Level
from ludicrous.SimpleInterface import SimpleInterface

class SampleMap(Level):
    WIDTH = 25
    HEIGHT = 6
    coded_grid = """\
gooooooooooooG
d#,......,,,.jooooooo
d##......,,,#:...*...
d#,......,,,.gooooooo
jooooooooooooJ"""
    #More than one symbol per type can be defined: these
    # can then be distinguished in the run code
    list_of_symbols = {"g":"wall_corner_nw", "G":"wall_corner_ne",
                       "j":"wall_corner_sw", "J":"wall_corner_se",
                       "d":"vwall", "o":"hwall", ":":"vfeature",
                       "*":"vfeature", " ":"space", ".":"floor1",
                       ",":"floor2", "#":"floor3"}
    starting_pt = (1, 1)
    title_window = "Basic Sample Ludicrous Map"

    def handle_move(self, target, playerobj):
        floorlevel = type(0)(self.get_index_grid(*playerobj.pt)[0][5:]) #XXX kludge/fragile/assumes
        nxtstat = self.get_index_grid(*target)[0]
        if nxtstat.startswith("floor"):
            newlevel = type(0)(nxtstat[5:])
            if (newlevel-floorlevel) <= 1:
                if (newlevel-floorlevel) == 1:
                    playerobj.myinterface.push_message("You climb up")
                elif (newlevel-floorlevel) < 0:
                    playerobj.myinterface.push_message("You jump down")
                return 1
            else:
                playerobj.myinterface.push_message("You try to climb but can't")
                return 0
        elif self.get_index_grid(*target)[1] == ":":
            kind, car = self.get_index_grid(*target)
            self.set_index_grid(("floor2", car), *target)
            playerobj.myinterface.push_message("The door opens")
            return 0
        elif self.get_index_grid(*target)[1] == "*":
            kind, car = self.get_index_grid(*target)
            self.set_index_grid(("floor1", car), *target)
            playerobj.myinterface.push_message("The door opens")
            return 0
        elif nxtstat == "space":
            playerobj.myinterface.push_message("You decide not to jump into the abyss")
            return 0
        else:
            playerobj.myinterface.push_message("You hit something")
            return 0

if __name__ == "__main__":
    from ludicrous.Game import Game
    import os, pickle
    _pp=pickle.Pickler
    class VerbosePickler(pickle.Pickler):
        def save(self, obj):
            print ("Pickling %s"%repr(obj)[:256])
            return _pp.save(self, obj)
    #pickle.Pickler=VerbosePickler
    class SampleMapGame(Game):
        _level=None
        InterfaceClass = SimpleInterface
        def level_initiate(self, playerobj):
            self._level=SampleMap(self)
            self._level.bring_to_front(playerobj, "starting")
        def levels_reown(self):
            self._level.reown(self)
        def level_restore(self, playerobj):
            self._level.bring_to_front(playerobj, "restoring")
        def level_advance(self, playerobj):
            raise RuntimeError("advancement without a level stack")
        def level_regress(self, playerobj):
            raise RuntimeError("regression without a level stack")
    if os.path.exists("s"):
        pickle.load(open("s","rU"))
    else:
        SampleMapGame()


