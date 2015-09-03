from repugeng.StaticClass import StaticClass

class TermcapUtility(StaticClass):
    """Rudimentary utility for reading integer (for now) terminal capabilities on POSIX."""
    @classmethod #Keeps pylint happy
    def _popen_read(cls, command):
        """Open a pipe to the stdout of a shell command."""
        try:
            #Newer API
            import subprocess
            return subprocess.Popen(command, shell=True, stdout=subprocess.PIPE).stdout
        except ImportError:
            #Older API
            import os
            return os.popen(command, "r")
    @classmethod #Keeps pylint happy
    def _system(cls, command):
        """Execute a command in the shell, return its return status."""
        try:
            #Newer API
            import subprocess
            return subprocess.call(command, shell=True)
        except ImportError:
            #Older API
            import os
            return os.system(command)
    @classmethod #Keeps pylint happy
    def _tput_get(cls, ticap, tccap):
        """Fallback method: attempt to get terminfo or termcap info via tput."""
        response = cls._popen_read("tput "+ticap).read()
        if not response:
            response = cls._popen_read("tput "+tccap).read()
        return response
    @classmethod #Keeps pylint happy
    def getnum(cls, ticap, tccap):
        """Attempt to get terminfo or termcap info via any available means."""
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
    @classmethod #Keeps pylint happy
    def dimensions(cls):
        """Return (width,height), negatives if either cannot be found."""
        width = cls.getnum("cols", "co")
        height = cls.getnum("lines", "li")
        return width, height

