import os
from repugeng.PosixBackend import PosixBackend
from repugeng.WconioWindowsBackend import WconioWindowsBackend
from repugeng.RpcBackend import RpcBackend

class BackendSelector(object):
    @staticmethod
    def __new__(*isnt,**interested): #pylint: disable=unused-argument
        raise TypeError("attempt to create instance of static class")
    dispatcher={"nt":[WconioWindowsBackend,RpcBackend],"posix":[PosixBackend,RpcBackend]}
    @classmethod
    def get_backend(cls,rpc=True):
        #rpc is True, False or -1
        #True: use it
        #False: don't use it if possible
        #-1: this *is* the remote, so definitely not!
        if rpc and (rpc>0):
            return RpcBackend()
        for i in cls.dispatcher[os.name]:
            if ((not rpc) or i!=RpcBackend) and i.works_p():
                if i==RpcBackend:
                    print ("No supported local backend, falling back to RPC.")
                    print ("(On Windows, WConio is required due to the lack of ANSI escapes.)")
                return i()
        raise ImportError("no supported backend.  On Windows, install WConio.")
