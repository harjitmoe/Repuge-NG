from ludicrous.GridObject import GridObject

class DijkstraMonster(GridObject):
    """An generic adversary which makes for the player.
    """
    tile = "adversary"
    name = "generic Dijkstra-map monster"
    appearance = "featureless monster"
    vitality = 5
    maxhp = 5
    projectiles = 0
    takes_damage = 1
    def initialise(self):
        self.add_handler(1, self.onetick)
    def can_throw(self, direction):
        if (not self.pt) or (not self.level):
            return 0
        #Given that it is not None, we gather that it is coords
        x, y = self.pt #pylint: disable = unpacking-non-sequence
        _w, _h = self.level.grid_dimens()
        while 1:
            if self.level.objgrid[x][y]:
                for obj in self.level.objgrid[x][y][:]:
                    if hasattr(obj, "myinterface") and obj.myinterface != None:
                        return 1
            adjacents = ([(x-1, y-1)] if x > 0 and y > 0 else []) \
                      + ([(x, y-1)] if y > 0 else []) \
                      + ([(x+1, y-1)] if x < (_w-1) and y > 0 else []) \
                      + ([(x+1, y)] if x < (_w-1) else []) \
                      + ([(x+1, y+1)] if x < (_w-1) and y < (_h-1) else []) \
                      + ([(x, y+1)] if y < (_h-1) else []) \
                      + ([(x-1, y+1)] if x > 0 and y < (_h-1) else []) \
                      + ([(x-1, y)] if x > 0 else [])
            if direction=="NW":
                target=(x-1,y-1)
            elif direction=="N":
                target=(x,y-1)
            elif direction=="NE":
                target=(x+1,y-1)
            elif direction=="E":
                target=(x+1,y)
            elif direction=="SE":
                target=(x+1,y+1)
            elif direction=="S":
                target=(x,y+1)
            elif direction=="SW":
                target=(x-1,y+1)
            elif direction=="W":
                target=(x-1,y)
            if target not in adjacents:
                break
            if not self.level.get_index_grid(*target)[0].startswith("floor"):
                break
            x, y = target
        return 0
    def onetick(self):
        if self.myinterface != None:
            return
        if self.vitality <= 0:
            self.die()
            return
        if not self.pt:
            return
        #Given that it is not None, we gather that it is coords
        x, y = self.pt #pylint: disable = unpacking-non-sequence
        _w, _h = self.level.grid_dimens()
        adjacents = ([(x-1, y-1)] if x > 0 and y > 0 else []) \
                  + ([(x, y-1)] if y > 0 else []) \
                  + ([(x+1, y-1)] if x < (_w-1) and y > 0 else []) \
                  + ([(x+1, y)] if x < (_w-1) else []) \
                  + ([(x+1, y+1)] if x < (_w-1) and y < (_h-1) else []) \
                  + ([(x, y+1)] if y < (_h-1) else []) \
                  + ([(x-1, y+1)] if x > 0 and y < (_h-1) else []) \
                  + ([(x-1, y)] if x > 0 else [])
        target = None
        target_height = 65535
        dm_grid = self.level.dm_grid
        if dm_grid == None:
            return
        for _x, _y in adjacents:
            if dm_grid[_x][_y] != self.level.dm_grid2[_x][_y]:
                continue # Player not visible
            if dm_grid[_x][_y] < target_height:
                target = (_x, _y)
                target_height = dm_grid[_x][_y]
        if target == None:
            return
        #
        for i in range(1): #pylint: disable = unused-variable
            if self.projectiles and (not self.empty()):
                for direction in ("NW","N","NE","E","SE","S","SW","W"):
                    if self.can_throw(direction):
                        self.contents[0].throw(direction, self.pt, self.level)
                        return
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
        else: #i.e. ran to completion with no break
            return #stuck, cannot move
        self.place(*target)
        self.level.redraw()
