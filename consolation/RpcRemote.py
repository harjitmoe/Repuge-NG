try:
    from SimpleXMLRPCServer import SimpleXMLRPCServer #pylint: disable = import-error
except ImportError:
    #3k
    from xmlrpc.server import SimpleXMLRPCServer #pylint: disable = import-error
from consolation.DisplaySelector import DisplaySelector

__copying__="""
This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/."""

class RpcRemote(object):
    """An XMLRPC remote process at the service of an RpcDisplay."""
    def __init__(self):
        self.backend = DisplaySelector.get_display(rpc=-1)
        port = int(self.backend.ask_question("Use port: "))
        self.server = SimpleXMLRPCServer(("localhost", port), allow_none=True, logRequests=False)
        self.server.register_introspection_functions()
        self.server.register_multicall_functions()
        self.server.register_instance(self.backend, False)
        self.server.serve_forever()
