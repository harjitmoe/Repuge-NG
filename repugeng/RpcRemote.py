try:
    from SimpleXMLRPCServer import SimpleXMLRPCServer
except ImportError:
    from xmlrpc.server import SimpleXMLRPCServer #3k
from repugeng.BackendSelector import BackendSelector
class RpcRemote(object):
    def __init__(self):
        self.backend=BackendSelector.get_backend(rpc=False)
        port=int(self.backend.ask_question("Use port: "))
        self.server=SimpleXMLRPCServer(("localhost", port),allow_none=True,logRequests=False)
        self.server.register_introspection_functions()
        self.server.register_multicall_functions()
        self.server.register_instance(self.backend,False)
        self.server.serve_forever()
