import sys
from repugeng.Backend import Backend
from repugeng.compat3k import *
class RpcBackend(Backend):
    _plot_cache=None
    _already=None
    def __init__(self):
        try:
            import xmlrpclib
        except ImportError:
            import xmlrpc.client as xmlrpclib #3k
        host=raw_input("Host of next remote (blank for localhost): ").strip() or "localhost"
        port=int(raw_input("Port used: "))
        self.backend=xmlrpclib.ServerProxy("http://%s:%d/"%(host,port),allow_none=True)
        self._plot_cache=[]
        self._already={}
    def __getattribute__(self,attr):
        if attr.startswith("__"):
            return object.__getattribute__(self,attr)
        if attr in ("backend","plot_tile","flush_plots","goto_point","_plot_cache","_already"):
            return object.__getattribute__(self,attr)
        return getattr(self.backend,attr)
    def plot_tile(self,y,x,tile_id):
        if ((x,y) in self._already) and (self._already[(x,y)]==tile_id):
            return
        self._already[(x,y)]=tile_id
        self._plot_cache.append({"methodName":"plot_tile","params":(y,x,tile_id)})
    def goto_point(self,x,y):
        self._plot_cache.append({"methodName":"goto_point","params":(x,y)})
    def flush_plots(self):
        self.system.multicall(self._plot_cache)
        self._plot_cache=[]
    @staticmethod
    def works_p():
        try:
            import xmlrpclib
        except:
            try:
                import xmlrpc.client as xmlrpclib #3k
            except:
                return False
        return True
