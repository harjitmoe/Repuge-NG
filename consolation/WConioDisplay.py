#Stuff which might not be present on system is to be imported in methods.
from consolation.BaseConioDisplay import BaseConioDisplay

__copying__="""
Written by Thomas Hori

This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/."""

class WConioDisplay(BaseConioDisplay):
    """Binding for Windows via the WConio extension for Python."""
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
