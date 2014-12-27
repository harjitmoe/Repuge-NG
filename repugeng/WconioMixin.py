#Stuff which might not be present on system is to be imported in methods.

class WconioMixin(object):
    def _conio_gotoxy(self,x,y):
        import WConio
        WConio.gotoxy(x,y)
    def _conio_settitle(self,s):
        import WConio
        WConio.settitle(s)
    def _conio_getkey(self):
        import WConio
        return WConio.getkey()
    def _conio_puttext(self,a,b,c,d,t):
        import WConio
        WConio.puttext(a,b,c,d,t)
    def _conio_textcolor(self,colour):
        import WConio
        WConio.textcolor(colour)

