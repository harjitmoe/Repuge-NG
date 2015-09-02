#Stuff which might not be present on system is to be imported in methods.
from repugeng.WindowsBackend import WindowsBackend

class WconioWindowsBackend(WindowsBackend):
    @staticmethod
    def works_p():
        try:
            import WConio #pylint: disable = import-error, unused-variable
        except ImportError:
            return 0
        else:
            return 1
    #
    def _conio_gotoxy(self, x, y):
        import WConio #pylint: disable = import-error
        WConio.gotoxy(x, y)
    def _conio_settitle(self, s):
        import WConio #pylint: disable = import-error
        WConio.settitle(s)
    def _conio_getkey(self):
        import WConio #pylint: disable = import-error
        return WConio.getkey()
    def _conio_puttext(self, a, b, c, d, t):
        import WConio #pylint: disable = import-error
        WConio.puttext(a, b, c, d, t)
    def _conio_textcolor(self, colour):
        import WConio #pylint: disable = import-error
        WConio.textcolor(colour)
