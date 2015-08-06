import sys,xmlrpclib
from SimpleXMLRPCServer import SimpleXMLRPCServer
from repugeng.BackendSelector import BackendSelector
class RpcInterfaceClient(object):
    def __init__(self):
        self.client=SimpleXMLRPCServer(("localhost", 8000),allow_none=True,logRequests=False)
        self.client.register_instance(self,False)
        self._pt=None
        self._grid=None
        self._fobjgrid=None
        self.backend=BackendSelector.get_backend()
        self.client.serve_forever()
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
        return self.generic_coords,self._grid,self._fobjgrid
    def get_viewport_pt(self):
        return self._pt
    def redraw(self,pt,grid,fobjgrid):
        """Draw the map (grid and objgrid).
        
        Presently this, by default, draws grid and (above it) objgrid at once
        and draws the entire grid.
        
        Unless you are a FOV/LOS engine, you probably don't want to override 
        this."""
        self._pt=pt
        self._grid=grid
        self._fobjgrid=fobjgrid
        if self._pt:
            self.backend.goto_point(*self.get_viewport_pt())
        colno=0
        for coordscol,col,col2 in zip(*self.get_viewport_grids()):
            rowno=0
            for coords,row,row2 in zip(coordscol,col,col2):
                #print rowno,colno,col
                if row2:
                    self.backend.plot_tile(colno,rowno,row2[-1])
                elif row:
                    self.backend.plot_tile(colno,rowno,row[0])
                rowno+=1
            colno+=1
    def level_load(self,title,grid):
        try:
            self.backend.set_window_title("[CLIENT] "+title)
        except NotImplementedError:
            pass
        self.generic_coords=map(lambda h:zip(*enumerate(h))[0],grid)
        self.generic_coords=map(lambda x:map((lambda y,x=x[0]:(x,y)),x[1]), enumerate(self.generic_coords))
    def flush_fov(self):
        """Bin any cached info about the current level FOV."""
        pass
    def close(self):
        sys.exit()
    def push_message(self,s):
        return self.backend.push_message(s)
    def ask_question(self,s):
        return self.backend.ask_question(s)
    def slow_ask_question(self,s,p=""):
        return self.backend.ask_question(s,p)
    def get_key_event(self):
        return self.backend.get_key_event()
