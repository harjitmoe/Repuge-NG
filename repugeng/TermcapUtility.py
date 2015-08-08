class TermcapUtility(object):
    """Rudimentary utility for reading integer (for now) terminal capabilities on POSIX."""
    @staticmethod
    def __new__(cls,*a,**kw):
        raise TypeError("attempt to create instance of static class")
    #
    @staticmethod
    def _popen_read(command):
        try:
            #Newer API
            import subprocess
            return subprocess.Popen(command,shell=True,stdout=subprocess.PIPE).stdout
        except ImportError:
            #Older API
            import os
            return os.popen(command,"r")
    @staticmethod
    def _system(command):
        try:
            #Newer API
            import subprocess
            return subprocess.call(command,shell=True)
        except ImportError:
            #Older API
            import os
            return os.system(command)
    @classmethod
    def _tput_get(cls,ticap,tccap):
        response=cls._popen_read("tput "+ticap).read()
        if not response:
            response=cls._popen_read("tput "+tccap).read()
        return response
    @classmethod
    def getnum(cls,ticap,tccap):
        try:
            #Use an API to access terminfo - preferred
            import curses
            return curses.tigetnum(ticap)
        except ImportError:
            #No Curses.  Curses!
            response=cls._tput_get(ticap,tccap).strip()
            try:
                return int(response)
            except:
                return -2
    @classmethod
    def dimensions(cls):
        width=cls.getnum("cols","co")
        height=cls.getnum("lines","li")
        return width,height
