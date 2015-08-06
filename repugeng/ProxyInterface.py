import sys,xmlrpclib,SimpleXMLRPCServer
from repugeng.SimpleInterface import SimpleInterface
class ProxyInterface(SimpleInterface):
    def __init__(self,playerobj,backend=None,debug_dummy=False):
        self.server=SimpleXMLRPCServer(("localhost", 8001))
        self.server.register_instance(self)
        self.remote=xmlrpclib.ServerProxy("http://localhost:8000/")
        self.remote.init(debug_dummy,8001)
        self.level_map=[]
    def get_offsets(self):
        """Used for LOS optimisation if only part of map visible."""
        return self.remote.get_offsets()
    def get_viewport_grids(self):
        return self.remote.get_viewport_grids()
    def get_viewport_pt(self):
        return self.remote.get_viewport_pt()
    def redraw(self):
        """Draw the map (grid and objgrid).
        
        Presently this, by default, draws grid and (above it) objgrid at once
        and draws the entire grid.
        
        Unless you are a FOV/LOS engine, you probably don't want to override 
        this."""
        return self.remote.redraw()
    def level_rebase(self,newlevel):
        """Link to new level, and bin any cached info about the current level."""
        if newlevel in self.level_map:
            codelevel=self.level_map.index(newlevel)
        else:
            codelevel=len(self.level_map)
            self.level_map.append(codelevel)
        return self.remote.level_rebase(codelevel)
    def flush_fov(self):
        """Bin any cached info about the current level FOV."""
        pass
    def close(self):
        sys.exit()
    def _get_title(self):
        return self.level.title_window
    def _get_grid(self):
        return self.level.grid
    def _get_flat_objgrid(self):
        out=[]
        for col in self.level.objgrid:
            outcol=[]
            for pile in col:
                outpile=map(lambda x:x.tile,pile)
                outcol.append(outpile)
            out.append(outcol)
        return out
    def _get_pt(self):
        return self.playerobj.pt
