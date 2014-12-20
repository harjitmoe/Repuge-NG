import os
from PosixBackend import PosixBackend
from WconioWindowsBackend import WconioWindowsBackend

class BackendSelector(object):
    @staticmethod
    def __new__(cls,*a,**kw):
        raise TypeError("attempt to create instance of static class")
    dispatcher={"nt":[WconioWindowsBackend],"posix":[PosixBackend]}
    @classmethod
    def get_backend(cls):
        for i in cls.dispatcher[os.name]:
            if i.works_p():
                return i()
        raise ImportError("no supported backend.  On Windows, install WConio.")
