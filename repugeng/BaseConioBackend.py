from repugeng.BaseConsoleBackend import BaseConsoleBackend
from repugeng.ConioTiles import ConioTiles
from repugeng.compat3k import * #pylint: disable = redefined-builtin, wildcard-import, unused-wildcard-import

class BaseConioBackend(BaseConsoleBackend):
    """Partially implementing base class"""
    _tiles_class = ConioTiles
    def goto_point(self, x, y):
        del self.point[:]
        self.point.extend([x, y])
        self._conio_gotoxy(x, y)
    def set_window_title(self, title):
        self._conio_settitle(bytes(title))
    def get_key_event(self):
        self.dump_messages()
        return self._conio_getkey()
    def _plot_character(self, x, y, c):
        self._conio_puttext(x, y, x, y, bytes(c))
    def _engage_message_formatting(self):
        self._conio_textcolor(0xF)
    #In subclasses, using e.g. WConio (binding to Windows port of conio)
    #or else implementing conio on Windows with help of ctypes
    #or using a conio extension under DOS (unlikely) etc...
    def _conio_gotoxy(self, x, y):
        raise NotImplementedError
    def _conio_settitle(self, s):
        raise NotImplementedError
    def _conio_getkey(self):
        raise NotImplementedError
    def _conio_puttext(self, a, b, c, d, t):
        raise NotImplementedError
    def _conio_textcolor(self, colour):
        raise NotImplementedError
