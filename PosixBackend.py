import sys,termios
from ConsoleBackend import ConsoleBackend
from PosixTiles import PosixTiles
from compat3k import *

class PosixBackend(ConsoleBackend):
    _tiles_class=PosixTiles
    def __init__(self,*a,**kw):
        self._plotcache={}
        super(PosixBackend,self).__init__(*a,**kw)
        #Because this is Linux it behooveth thee (thou?) to clear the screen first
        print("\x1b[2J")
    def _engage_message_formatting(self):
        sys.stderr.write("\x1b[1;37m")
    def _end_message_formatting(self):
        sys.stderr.write("\x1b[m") #reset colour
        sys.stderr.flush()
        sys.stderr.write("\x1b[1;37m")
    def goto_point(self,x,y):
        self.point[:]=x,y
        sys.stderr.write("\x1B[%d;%dH"%(y+1,x+1))
    def set_window_title(self,title):
        sys.stderr.write("\x1b]0;%s\x1b\\"%title)
    def get_key_event(self):
        #self._plotcache={} #Get rid of the misechoed keystrokes
        s=self._getch()
        #outputtext(`s`)
        if s=="\x1b":
            s=self._getch()
            #outputtext(`s`)
            if s=="[":
                s=self._getch()
                #outputtext(`s`)
                if s=="A":
                    s="up"
                elif s=="B":
                    s="down"
                elif s=="C":
                    s="right"
                elif s=="D":
                    s="left"
            #XXX else undefined behaviour (in practice just skipping the \x1b)
        return s
    def _plot_character(self,y,x,c):
        if ((y,x) not in plotcache) or (plotcache[(y,x)]!=c):
            sys.stderr.write("\x1B[?25l") #hide cursor, ? means extension, and that's a lowercase L
            sys.stderr.write("\x1B[%d;%dH%s"%(y+1,x+1,c))
            sys.stderr.write("\x1B[m") #reset colour
            sys.stderr.write("\x1B[?25h") #show cursor, ? means extension
            sys.stderr.flush()
            plotcache[(y,x)]=c
        self.goto_point(*pt)
    #
    def _getch(self,reset_afterwards=0): #avoid misechoed keystrokes between checks
        attrs=termios.tcgetattr(0);
        termios.tcsetattr(0,termios.TCSADRAIN,attrs[:3]+[attrs[3]&(~termios.ICANON)&(~termios.ECHO)]+attrs[4:])
        termios.tcdrain(0)
        char=sys.stdin.read(1)
        if reset_afterwards:
            termios.tcsetattr(0,termios.TCSADRAIN,attrs)
        return char
    def _reset_terminal(self):
        attrs=termios.tcgetattr(0);
        termios.tcsetattr(0,termios.TCSADRAIN,attrs[:3]+[attrs[3]|termios.ICANON|termios.ECHO]+attrs[4:])
        termios.tcdrain(0)
