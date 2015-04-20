from repugeng.BackendSelector import BackendSelector
class SimpleInterface(object):
    def __init__(self,playerobj,backend=None,debug_dummy=False):
        self.playerobj=playerobj
        self.level=playerobj.level
        #
        if not debug_dummy:
            self.level.bug_report[__name__]={}
            if backend:
                self.backend=backend
            else:
                self.backend=BackendSelector.get_backend()
            #Attempt to set title
            try:
                self.backend.set_window_title(self.level.title_window)
            except NotImplementedError:
                pass
    def redraw(self):
        """Draw the map (grid and objgrid).
        
        Presently this, by default, draws grid and (above it) objgrid at once
        and draws the entire grid.
        
        Unless you are a FOV engine, you probably don't want to override 
        this."""
        if self.playerobj.pt:
            self.backend.goto_point(*self.playerobj.pt)
        colno=0
        for col,col2 in zip(self.level.grid,self.level.objgrid):
            rowno=0
            for row,row2 in zip(col,col2):
                #print rowno,colno,col
                if row2:
                    self.backend.plot_tile(colno,rowno,row2[-1].tile)
                elif row:
                    self.backend.plot_tile(colno,rowno,row[0])
                rowno+=1
            colno+=1
        