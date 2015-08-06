import os
from repugeng.PosixBackend import PosixBackend
from repugeng.WconioWindowsBackend import WconioWindowsBackend
from repugeng.RpcBackend import RpcBackend

class BackendSelector(object):
    @staticmethod
    def __new__(cls,*a,**kw):
        raise TypeError("attempt to create instance of static class")
    dispatcher={"nt":[WconioWindowsBackend,RpcBackend],"posix":[PosixBackend,RpcBackend]}
    @classmethod
    def get_backend(cls,rpc=True):
        if rpc:
            return RpcBackend()
        for i in cls.dispatcher[os.name]:
            if i.works_p():
                return i()
        raise ImportError("no supported backend.  On Windows, install WConio.")
