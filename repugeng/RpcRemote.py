try:
    from SimpleXMLRPCServer import SimpleXMLRPCServer #pylint: disable=import-error
except ImportError:
    #3k
    from xmlrpc.server import SimpleXMLRPCServer #pylint: disable=import-error
from repugeng.BackendSelector import BackendSelector
class RpcRemote(object):
    def __init__(self):
        self.backend=BackendSelector.get_backend(rpc=-1)
        port=int(self.backend.ask_question("Use port: "))
        self.server=SimpleXMLRPCServer(("localhost", port),allow_none=True,logRequests=False)
        self.server.register_introspection_functions()
        self.server.register_multicall_functions()
        self.server.register_instance(self.backend,False)
        self.server.serve_forever()
