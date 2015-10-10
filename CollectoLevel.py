import sys, random, math
from ludicrous.GeneratedLevel import GeneratedLevel
from ludicrous.MultilevelStorage import MultilevelStorage
from CollectoObject import CollectoObject

class CollectoLevel(GeneratedLevel):
    coded_grid = None
    title_window = "Ludicrous Collecto"

    def get_new_point(self):
        return random.choice(self.gamut)

    def initmap(self):
        #Initialise scoring storage
        self.score = MultilevelStorage("collecto_score")
        self.score.initialise_property("myscore", 0)
        self.score.initialise_property("mymoves", 0)
        #Generate map
        self.genmap()
        self.starting_pt = self.get_new_point()
        #Put collectones in unique locations
        for junk in range(int(math.sqrt(len(self.gamut)))):
            CollectoObject(self.game).place(*self.get_new_point()+(self,))
        pos_x, pos_y = self.get_new_point()
        self.grid[pos_x][pos_y] = ("staircase", "%")
        #
        self.nan = 0
        self.children = []

    def handle_move(self, target, playerobj):
        try: #XXX kludge/fragile/assumes
            floorlevel = type(0)(self.get_index_grid(*playerobj.pt)[0][5:])
        except ValueError:
            floorlevel = 1 #Needed or mazed subclass breaks
        nxtstat = self.get_index_grid(*target)[0]
        if self.objgrid[target[0]][target[1]]:
            for obj in self.objgrid[target[0]][target[1]][:]:
                if isinstance(obj, CollectoObject):
                    obj.handle_contact(playerobj)
        elif nxtstat.startswith("floor"):
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
        elif nxtstat == "staircase":
            playerobj.myinterface.push_message("You find a staircase (use Return"
                                               " (enter) to descend).")
            return 1
        elif nxtstat == "space":
            playerobj.myinterface.push_message("You hit the tunnel wall.")
            return 0
        else:
            playerobj.myinterface.push_message("You hit something.")
            return 0

    def handle_command(self, e, playerobj):
        if e in (">", "\r", "\n", "\r\n", " ", "return", "enter", "space") \
           and self.get_index_grid(*playerobj.pt)[0] == "staircase":
            self.game.level_advance(playerobj)
            sys.exit()
        elif e == "#quit":
            sys.exit()
