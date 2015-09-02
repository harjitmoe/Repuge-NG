from repugeng.Backend import Backend
from repugeng.compat3k import * #pylint: disable=redefined-builtin,wildcard-import,unused-wildcard-import
class RpcBackend(Backend):
    #pylint: disable=abstract-method,super-init-not-called
    _plot_cache=None
    _already=None
    _dimensions=None
    def __init__(self):
        try:
            import xmlrpclib #pylint: disable=import-error
        except ImportError:
            #3k
            import xmlrpc.client as xmlrpclib #pylint: disable=import-error
        host=raw_input("Host of next remote (blank for localhost): ").strip() or "localhost"
        port=int(raw_input("Port used: "))
        self.backend=xmlrpclib.ServerProxy("http://%s:%d/"%(host,port),allow_none=True)
        self._plot_cache=[]
        self._already={}
        self._dimensions=self.backend.get_dimensions()
    def __getattribute__(self,attr):
        if attr.startswith("__"):
            return object.__getattribute__(self,attr)
        if attr in ("backend","plot_tile","flush_plots","goto_point","_plot_cache","_already","get_dimensions","_dimensions"):
            return object.__getattribute__(self,attr)
        return getattr(self.backend,attr)
    def plot_tile(self,y,x,tile_id):
        if ((x,y) in self._already) and (self._already[(x,y)]==tile_id):
            #This optimisation is at this end as it takes *much* longer to send a
            #plot_tile request over XMLRPC than it does to execute it.
            return
        if ((x,y) not in self._already) and (tile_id=="space"):
            #This optimisation is at this end as it takes *much* longer to send a
            #plot_tile request over XMLRPC than it does to execute it.
            return
        self._already[(x,y)]=tile_id
        self._plot_cache.append({"methodName":"plot_tile","params":(y,x,tile_id)})
    def goto_point(self,x,y):
        self._plot_cache.append({"methodName":"goto_point","params":(x,y)})
    def flush_plots(self):
        self.system.multicall(self._plot_cache)
        self._plot_cache=[]
    def get_dimensions(self):
        return self._dimensions
    @staticmethod
    def works_p():
        try:
            import xmlrpclib #pylint: disable=import-error,unused-variable
        except ImportError:
            try:
                #3k
                import xmlrpc.client as xmlrpclib #pylint: disable=import-error,unused-variable
            except ImportError:
                return False
        return True
