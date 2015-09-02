from repugeng.StaticClass import StaticClass

class TermcapUtility(StaticClass):
    """Rudimentary utility for reading integer (for now) terminal capabilities on POSIX."""
    def _popen_read(cls, command):
        try:
            #Newer API
            import subprocess
            return subprocess.Popen(command, shell=True, stdout=subprocess.PIPE).stdout
        except ImportError:
            #Older API
            import os
            return os.popen(command, "r")
    def _system(cls, command):
        try:
            #Newer API
            import subprocess
            return subprocess.call(command, shell=True)
        except ImportError:
            #Older API
            import os
            return os.system(command)
    def _tput_get(cls, ticap, tccap):
        response = cls._popen_read("tput "+ticap).read()
        if not response:
            response = cls._popen_read("tput "+tccap).read()
        return response
    def getnum(cls, ticap, tccap):
        try:
            #Use an API to access terminfo - preferred
            import curses
            curses.setupterm() #pylint: disable = no-member
            return curses.tigetnum(ticap) #pylint: disable = no-member
        except ImportError:
            #No Curses.  Curses!
            response = cls._tput_get(ticap, tccap).strip()
            try:
                return int(response)
            except ValueError:
                return -2
    def dimensions(cls):
        width = cls.getnum("cols", "co")
        height = cls.getnum("lines", "li")
        return width, height

