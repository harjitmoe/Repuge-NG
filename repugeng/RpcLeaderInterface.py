import sys,xmlrpclib,thread
from SimpleXMLRPCServer import SimpleXMLRPCServer
from repugeng.SimpleInterface import SimpleInterface
from repugeng.BackendSelector import BackendSelector
class RpcLeaderInterface(SimpleInterface):
    #Semantically public
    def __init__(self,playerobj,backend=None,debug_dummy=False):
        if not debug_dummy:
            if backend:
                self.backend=backend
            else:
                self.backend=BackendSelector.get_backend()
        port=int(self.backend.ask_question("Port used by remote: "))
        self.remote=xmlrpclib.ServerProxy("http://localhost:%d/"%port,allow_none=True)
        self.playerobj=playerobj
    def redraw(self):
        """Draw the map (grid and objgrid).
        
        Presently this, by default, draws grid and (above it) objgrid at once
        and draws the entire grid.
        
        Unless you are a FOV/LOS engine, you probably don't want to override 
        this."""
        return self.remote.redraw(self.playerobj.pt,self.level.grid,self.get_flat_objgrid())
    def level_rebase(self,newlevel):
        """Link to new level, and bin any cached info about the current level."""
        self.level=newlevel
        try:
            self.backend.set_window_title("[LEADER] "+self.level.title_window)
        except NotImplementedError:
            pass
        return self.remote.level_load(self.level.title_window,self.level.grid)
    def flush_fov(self):
        """Bin any cached info about the current level FOV."""
        return self.remote.flush_fov()
    def push_message(self,s):
        return self.remote.push_message(s)
    def ask_question(self,s):
        return self.remote.ask_question(s)
    def slow_ask_question(self,s,p=""):
        return self.remote.ask_question(s,p)
    def get_key_event(self):
        return self.remote.get_key_event()
    def close(self):
        self.remote.close()
        sys.exit() #For now
    #Semantically private
    remote=None
    def get_flat_objgrid(self):
        out=[]
        for col in self.level.objgrid:
            outcol=[]
            for pile in col:
                outpile=map(lambda x:x.tile,pile)
                outcol.append(outpile)
            out.append(outcol)
        return out
