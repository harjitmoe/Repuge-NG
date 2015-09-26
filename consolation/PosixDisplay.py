import sys
from consolation.BaseConsoleDisplay import BaseConsoleDisplay
from consolation.PosixTiles import PosixTiles
from consolation.TermcapUtility import TermcapUtility

class PosixDisplay(BaseConsoleDisplay):
    """Display for POSIX (GNU, OSX et cetera) via ANSI escapes, termios and optionally
    curses/termcap/terminfo."""
    _tiles_class = PosixTiles
    def __init__(self, *a, **kw):
        self._plotcache = {}
        super(PosixDisplay, self).__init__(*a, **kw)
        #Clear the screen
        print("\x1b[2J") #pylint: disable = superfluous-parens
    @staticmethod
    def works_p():
        try:
            import termios, os #pylint: disable = import-error, unused-variable
            return os.name == "posix"
        except ImportError:
            return 0
    def _engage_message_formatting(self):
        sys.stderr.write("\x1b[1;37m")
    def _end_message_formatting(self):
        sys.stderr.write("\x1b[m")
        sys.stderr.flush()
        self._engage_message_formatting()
    def goto_point(self, x, y):
        del self.point[:]
        self.point.extend([x, y])
        sys.stderr.write("\x1B[%d;%dH"%(y+1, x+1))
    def set_window_title(self, title):
        sys.stderr.write("\x1b]0;"+title+"\x1b\\")
    def get_key_event(self):
        self.dump_messages()
        s = self._getch()
        if s != "\x1B":
            return s
        s += self._getch()
        c = self._getch()
        while ord(c) in list(range(32,48)):
            s += c
            c = self._getch()
        s += c #Terminator character
        if s[-1] == "A":
            return "up"
        elif s[-1] == "B":
            return "down"
        elif s[-1] == "C":
            return "right"
        elif s[-1] == "D":
            return "left"
        return s
    def _plot_character(self, x, y, c):
        if (x, y) not in self._plotcache:
            self._plotcache[(x, y)] = " "
        if self._plotcache[(x, y)] == c:
            return
        rx, ry = self.point
        sys.stderr.write("\x1B%d;%dH%s\x1B%d;%dH\x1B[m" % (y+1, x+1, c, ry+1, rx+1))
        sys.stderr.flush()
    #
    def _getch(self, reset_afterwards=0): #avoid misechoed keystrokes between checks
        #Note: this function may be copyrighted by KSP.
        #To be rewritten.
        import termios  #pylint: disable = import-error
        attrs = termios.tcgetattr(0)
        termios.tcsetattr(0, termios.TCSADRAIN, \
                          attrs[:3]+[attrs[3]&(~termios.ICANON)&(~termios.ECHO)]+attrs[4:])
        termios.tcdrain(0)
        char = sys.stdin.read(1)
        if reset_afterwards:
            termios.tcsetattr(0, termios.TCSADRAIN, attrs)
        return char
    def _reset_terminal(self):
        #Note: this function may be copyrighted by KSP.
        #To be rewritten.
        import termios  #pylint: disable = import-error
        attrs = termios.tcgetattr(0)
        termios.tcsetattr(0, termios.TCSADRAIN, \
                          attrs[:3]+[attrs[3]|termios.ICANON|termios.ECHO]+attrs[4:])
        termios.tcdrain(0)
    def get_dimensions(self):
        return TermcapUtility.dimensions()

