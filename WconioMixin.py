import WConio
from compat3k import *

class WconioMixin(object):
    def _conio_gotoxy(self,x,y):
        WConio.gotoxy(x,y)
    def _conio_settitle(self,s):
        WConio.settitle(s)
    def _conio_getkey(self):
        return WConio.getkey()
    def _conio_puttext(a,b,c,d,t):
        WConio.puttext(a,b,c,d,t)

