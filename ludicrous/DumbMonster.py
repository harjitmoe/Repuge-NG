from ludicrous.GridObject import GridObject
import random

__copying__="""
Written by Thomas Hori

This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/."""

class DumbMonster(GridObject):
    """An generic adversary, random in its movements.
    """
    tile = "adversary"
    name = "unspecified monster"
    appearance = "featureless monster"
    vitality = 5
    maxhp = 5
    takes_damage = 1
    def initialise(self):
        self.insert(GridObject(self.game))
        self.insert(GridObject(self.game))
        self.insert(GridObject(self.game))
        self.add_handler(1, self.onetick)
    def onetick(self):
        if self.myinterface != None:
            return
        if self.vitality <= 0:
            self.die()
            return
        type_ = random.randrange(9)
        for i in range(1): #pylint: disable = unused-variable
            if type_ == 0:
                target = (self.pt[0], self.pt[1]+1)
            if type_ == 1:
                target = (self.pt[0]+1, self.pt[1])
            if type_ == 2:
                target = (self.pt[0], self.pt[1]-1)
            if type_ == 3:
                target = (self.pt[0]-1, self.pt[1])
            if type_ == 4:
                target = (self.pt[0], self.pt[1])
            if type_ == 5:
                target = (self.pt[0]+1, self.pt[1]+1)
            if type_ == 6:
                target = (self.pt[0]-1, self.pt[1]-1)
            if type_ == 7:
                target = (self.pt[0]-1, self.pt[1]+1)
            if type_ == 8:
                target = (self.pt[0]+1, self.pt[1]-1)
            try: #XXX kludge/fragile/assumes
                floorlevel = type(0)(self.level.get_index_grid(*self.pt)[0][5:])
            except ValueError:
                floorlevel = 1 #Needed or mazed subclass breaks
            nxtstat = self.level.get_index_grid(*target)[0]
            if self.level.objgrid[target[0]][target[1]]:
                for obj in self.level.objgrid[target[0]][target[1]][:]:
                    if hasattr(obj, "myinterface") and obj.myinterface != None:
                        if type(self) in obj.known: #pylint: disable = unidiomatic-typecheck
                            obj.myinterface.push_message("The %s hits!"%self.name)
                        else:
                            obj.myinterface.push_message("The %s hits!"%self.appearance)
                        obj.vitality -= 1
                        return
            elif nxtstat.startswith("floor") or (nxtstat in ("vfeature_open","hfeature_open")):
                newlevel = type(0)(nxtstat[5:])
                if (newlevel-floorlevel) <= 1:
                    break
            type_ += 1
            type_ %= 4
        else: #i.e. ran to completion with no break
            return #stuck, cannot move
        self.place(*target)
        self.level.redraw()
