from repugeng.GridObject import GridObject
from repugeng.PlayableObject import PlayableObject
from repugeng.Container import Container
import random

class DijkstraMonster(PlayableObject):
    """An generic adversary which makes for the player.
    """
    tile="adversary"
    name="generic Dijkstra-map monster"
    appearance="featureless monster"
    vitality=5
    maxhp=5
    def initialise_playable(self):
        """Just been spawned.  Do what?"""
        self.inventory=Container(self.level)
        self.inventory.insert(GridObject(self.level))
        self.inventory.insert(GridObject(self.level))
        self.inventory.insert(GridObject(self.level))
        self.add_handler(1,self.onetick)
    def _grid_dimens(self):
        width=len(self.level.grid)
        height=0
        for col in self.level.grid:
            if len(col)>height:
                height=len(col)
        return width,height
    def onetick(self):
        if self.myinterface!=None:
            return
        if self.vitality<=0:
            self.die()
            return
        _w,_h=self._grid_dimens()
        dm_grid=[list(i) for i in ([65534]*_h,)*_w]
        for i in self.level.child_interfaces:
            if hasattr(i,"playerobj") and hasattr(i.playerobj,"pt") and i.playerobj.pt:
                _x,_y=i.playerobj.pt
                dm_grid[_x][_y]=0
        changed=1
        while changed==1:
            changed=0
            for x in range(_w):
                h=len(self.level.grid[x])
                for y in range(h):
                    if not self.level.objgrid[x][y] and (self.level.grid[x][y][0].endswith("_open") or self.level.grid[x][y][0].startswith("floor")):
                        adjacents = ([(x-1,y-1)] if x>0 and y>0 else []) \
                                  + ([(x,y-1)] if y>0 else []) \
                                  + ([(x+1,y-1)] if x<(_w-1) and y>0 else []) \
                                  + ([(x+1,y)] if x<(_w-1) else []) \
                                  + ([(x+1,y+1)] if x<(_w-1) and y<(h-1) else []) \
                                  + ([(x,y+1)] if y<(h-1) else []) \
                                  + ([(x-1,y+1)] if x>0 and y<(h-1) else []) \
                                  + ([(x-1,y)] if x>0 else [])
                        for _x,_y in adjacents:
                            possible=dm_grid[_x][_y]+1
                            if possible<dm_grid[x][y]:
                                changed=1
                                dm_grid[x][y]=possible
                                #DO NOT break here
        x,y=self.pt
        adjacents = ([(x-1,y-1)] if x>0 and y>0 else []) \
                  + ([(x,y-1)] if y>0 else []) \
                  + ([(x+1,y-1)] if x<(_w-1) and y>0 else []) \
                  + ([(x+1,y)] if x<(_w-1) else []) \
                  + ([(x+1,y+1)] if x<(_w-1) and y<(_h-1) else []) \
                  + ([(x,y+1)] if y<(_h-1) else []) \
                  + ([(x-1,y+1)] if x>0 and y<(_h-1) else []) \
                  + ([(x-1,y)] if x>0 else [])
        target=None
        target_height=65535
        for _x,_y in adjacents:
            if dm_grid[_x][_y]<target_height:
                target=(_x,_y)
                target_height=dm_grid[_x][_y]
        self.dm_grid=dm_grid
        #
        for i in range(1):
            try: #XXX kludge/fragile/assumes
                floorlevel=type(0)(self.level.get_index_grid(*self.pt)[0][5:])
            except ValueError:
                floorlevel=1 #Needed or mazed subclass breaks
            nxtstat=self.level.get_index_grid(*target)[0]
            if self.level.objgrid[target[0]][target[1]]:
                breakp=1
                for obj in self.level.objgrid[target[0]][target[1]][:]:
                    if hasattr(obj,"myinterface") and obj.myinterface!=None:
                        if type(self) in obj.known:
                            obj.myinterface.push_message("The %s hits!"%self.name)
                        else:
                            obj.myinterface.push_message("The %s hits!"%self.appearance)
                        obj.vitality-=1
                        return
                else:
                    breakp=0
                if breakp:
                    break
            elif nxtstat.startswith("floor"):
                newlevel=type(0)(nxtstat[5:])
                if (newlevel-floorlevel)<=1:
                    break
        else: #i.e. ran to completion with no break
            return #stuck, cannot move
        self.place(*target)
        self.level.redraw()
