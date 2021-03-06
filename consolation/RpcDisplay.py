from consolation.BaseDisplay import BaseDisplay
from consolation.Compat3k import Compat3k

#The "threading" module over-complicates things imo
try:
    from thread import allocate_lock #pylint: disable = import-error
except ImportError:
    #3k
    from _thread import allocate_lock #pylint: disable = import-error

__copying__="""
Written by Thomas Hori

This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/."""

class RpcDisplay(BaseDisplay):
    """Exports the Display API but, rather than implementing it (bar some
    optimisation measures), sends queries via XMLRPC to a remote process."""
    #pylint: disable = abstract-method, super-init-not-called
    _plot_cache = None
    _already = None
    _dimensions = None
    def __init__(self):
        try:
            import xmlrpclib #pylint: disable = import-error
        except ImportError:
            #3k
            import xmlrpc.client as xmlrpclib #pylint: disable = import-error
        class ClassicTransport(xmlrpclib.Transport):
            def make_connection(self, host):
                self._extra_headers = []
                self._connection = (None, None)
                r=xmlrpclib.Transport.make_connection(self, host)
                self._extra_headers = []
                self._connection = (None, None)
                return r
        host = Compat3k.prompt_user("Host of next remote (blank for localhost): ").strip() or "localhost"
        port = int(Compat3k.prompt_user("Port used: "))
        self.backend = xmlrpclib.ServerProxy("http://%s:%d/"%(host, port), allow_none=True, transport=ClassicTransport())
        self._plot_cache = []
        self._already = {}
        self._dimensions = self.backend.get_dimensions()
        self._lock = allocate_lock()
        self.rpc_remote_address = (host, port)
    def __getattribute__(self, attr):
        if attr.startswith("__"):
            return object.__getattribute__(self, attr)
        if attr in ("backend", "plot_tile", "flush_plots", "goto_point", "_plot_cache",
                    "_already", "get_dimensions", "_dimensions","_lock","rpc_remote_address"):
            return object.__getattribute__(self, attr)
        return getattr(self.backend, attr)
    def plot_tile(self, y, x, tile_id):
        #Optimisations are at this end as it takes *much* longer to send a
        #plot_tile request over XMLRPC than it does to execute it.
        if ((x, y) in self._already) and (self._already[(x, y)] == tile_id):
            return
        if ((x, y) not in self._already) and (tile_id == "space"):
            return
        self._already[(x, y)] = tile_id
        self._plot_cache.append({"methodName":"plot_tile", "params":(y, x, tile_id)})
    def goto_point(self, x, y):
        self._plot_cache.append({"methodName":"goto_point", "params":(x, y)})
    def flush_plots(self):
        self._lock.acquire()
        self.system.multicall(self._plot_cache)
        self._plot_cache = []
        self._lock.release()
    def get_dimensions(self):
        return self._dimensions
    @staticmethod
    def works_p():
        try:
            import xmlrpclib #pylint: disable = import-error, unused-variable
        except ImportError:
            try:
                #3k
                import xmlrpc.client as xmlrpclib #pylint: disable = import-error, unused-variable
            except ImportError:
                return False
        return True
