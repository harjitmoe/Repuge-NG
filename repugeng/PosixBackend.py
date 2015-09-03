import sys
from repugeng.BaseConsoleBackend import BaseConsoleBackend
from repugeng.PosixTiles import PosixTiles
from repugeng.TermcapUtility import TermcapUtility
from repugeng.compat3k import * #pylint: disable = redefined-builtin, wildcard-import, unused-wildcard-import

class PosixBackend(BaseConsoleBackend):
    """Backend for POSIX (GNU, OSX et cetera) via ANSI escapes, termios and optionally
    curses/termcap/terminfo."""
    _tiles_class = PosixTiles
    def __init__(self, *a, **kw):
        self._plotcache = {}
        super(PosixBackend, self).__init__(*a, **kw)
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
        #Note: this function may be copyrighted by KSP.
        #To be rewritten.
        self.dump_messages()
        s = self._getch()
        if s == "\x1b":
            s = self._getch()
            if s == "[":
                s = "0"
                while s == "0":
                    s = self._getch()
                if s == "A":
                    s = "up"
                elif s == "B":
                    s = "down"
                elif s == "C":
                    s = "right"
                elif s == "D":
                    s = "left"
            #XXX else undefined behaviour (in practice just skipping the \x1b)
        return s
    def _plot_character(self, x, y, c):
        #Note: this function may be copyrighted by KSP.
        #To be rewritten.
        if (((x, y) not in self._plotcache) and c != " ") or (self._plotcache[(x, y)] != c):
            sys.stderr.write("\x1B[?25l") #hide cursor, ? means extension, and that's a lowercase L
            sys.stderr.write("\x1B[%d;%dH%s"%(y+1, x+1, c))
            sys.stderr.write("\x1B[m") #reset colour
            sys.stderr.write("\x1B[?25h") #show cursor, ? means extension
            sys.stderr.flush()
            self._plotcache[(x, y)] = c
        self.goto_point(*self.point)
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

