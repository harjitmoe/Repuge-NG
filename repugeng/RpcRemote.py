import sys,xmlrpclib
from SimpleXMLRPCServer import SimpleXMLRPCServer
from repugeng.BackendSelector import BackendSelector
class RpcRemote(object):
    def __init__(self):
        self.backend=BackendSelector.get_backend()
        port=int(self.backend.ask_question("Use port: "))
        self.server=SimpleXMLRPCServer(("localhost", port),allow_none=True,logRequests=False)
        self.server.register_instance(self.backend,False)
        self.server.serve_forever()
