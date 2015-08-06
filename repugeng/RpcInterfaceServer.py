import sys,xmlrpclib,thread
from SimpleXMLRPCServer import SimpleXMLRPCServer
from repugeng.SimpleInterface import SimpleInterface
class RpcInterfaceServer(SimpleInterface):
    def __init__(self,playerobj,backend=None,debug_dummy=False):
        self.server=SimpleXMLRPCServer(("localhost", 8001),allow_none=True,logRequests=False)
        self.server.register_instance(self)
        thread.start_new_thread(self.server.serve_forever,())
        self.remote=xmlrpclib.ServerProxy("http://localhost:8000/",allow_none=True)
        self.remote.init(debug_dummy,8001)
        self.level_map=[]
        self.playerobj=playerobj
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
        return self.remote.redraw(self.get_pt(),self.get_grid(),self.get_flat_objgrid())
    def level_rebase(self,newlevel):
        """Link to new level, and bin any cached info about the current level."""
        self.level=newlevel
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
    def get_title(self):
        return self.level.title_window
    def get_grid(self):
        return self.level.grid
    def get_flat_objgrid(self):
        out=[]
        for col in self.level.objgrid:
            outcol=[]
            for pile in col:
                outpile=map(lambda x:x.tile,pile)
                outcol.append(outpile)
            out.append(outcol)
        return out
    def get_pt(self):
        return self.playerobj.pt
    def push_message(self,s):
        return self.remote.push_message(s)
    def ask_question(self,s):
        return self.remote.ask_question(s)
    def slow_ask_question(self,s,p=""):
        return self.remote.ask_question(s,p)
    def get_key_event(self):
        return self.remote.get_key_event()
