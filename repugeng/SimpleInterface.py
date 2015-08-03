import sys
from repugeng.BackendSelector import BackendSelector
class SimpleInterface(object):
    def __init__(self,playerobj,backend=None,debug_dummy=False):
        self.playerobj=playerobj
        self.level=playerobj.level
        self.game=playerobj.game
        #
        if not debug_dummy:
            self.game.bug_report[__name__]={}
            if backend:
                self.backend=backend
            else:
                self.backend=BackendSelector.get_backend()
    def get_offsets(self):
        """Used for LOS optimisation if only part of map visible."""
        width=79
        height=19
        offsetx=0
        roffsetx=width
        offsety=0
        roffsety=height
        return width,height,offsetx,offsety,roffsetx,roffsety
    def get_viewport_grids(self):
        return self.generic_coords,self.level.grid,self.level.objgrid
    def get_viewport_pt(self):
        return self.playerobj.pt
    def redraw(self):
        """Draw the map (grid and objgrid).
        
        Presently this, by default, draws grid and (above it) objgrid at once
        and draws the entire grid.
        
        Unless you are a FOV/LOS engine, you probably don't want to override 
        this."""
        if self.playerobj.pt:
            self.backend.goto_point(*self.get_viewport_pt())
        colno=0
        for coordscol,col,col2 in zip(*self.get_viewport_grids()):
            rowno=0
            for coords,row,row2 in zip(coordscol,col,col2):
                #print rowno,colno,col
                if row2:
                    self.backend.plot_tile(colno,rowno,row2[-1].tile)
                elif row:
                    self.backend.plot_tile(colno,rowno,row[0])
                rowno+=1
            colno+=1
    def level_rebase(self,newlevel):
        """Link to new level, and bin any cached info about the current level."""
        self.level=newlevel
        #Attempt to set title
        try:
            self.backend.set_window_title(self.level.title_window)
        except NotImplementedError:
            pass
        self.generic_coords=[zip(*enumerate(h))[0] for h in self.level.grid]
        self.generic_coords=[[(x,y) for y in h] for x,h in enumerate(self.generic_coords)]
    def flush_fov(self):
        """Bin any cached info about the current level FOV."""
        pass
    def close(self):
        sys.exit()
        