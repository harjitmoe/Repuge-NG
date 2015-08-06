import sys,xmlrpclib,thread
from SimpleXMLRPCServer import SimpleXMLRPCServer
from repugeng.SimpleInterface import SimpleInterface
from repugeng.BackendSelector import BackendSelector
class RpcLeaderInterface(SimpleInterface):
    #Semantically public
    def __init__(self,playerobj,backend=None,debug_dummy=False):
        if not debug_dummy:
            if backend:
                self.backend2=backend
            else:
                self.backend2=BackendSelector.get_backend()
        port=int(self.backend2.ask_question("Port used by remote: "))
        self.backend=xmlrpclib.ServerProxy("http://localhost:%d/"%port,allow_none=True)
        self.playerobj=playerobj
