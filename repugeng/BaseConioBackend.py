from repugeng.BaseConsoleBackend import BaseConsoleBackend
from repugeng.ConioTiles import ConioTiles
from repugeng.Compat3k import Compat3k

class BaseConioBackend(BaseConsoleBackend):
    """A class implementing Backend in terms of a semantically
    protected conio-style interface which it leaves abstract.
    """
    _tiles_class = ConioTiles
    def goto_point(self, x_coord, y_coord):
        del self.point[:]
        self.point.extend([x_coord, y_coord])
        self._conio_gotoxy(x_coord, y_coord)
    def set_window_title(self, title):
        self._conio_settitle(Compat3k.str_to_bytes(title))
    def get_key_event(self):
        self.dump_messages()
        return self._conio_getkey()
    def _plot_character(self, y_coord, x_coord, character):
        self._conio_puttext(x_coord, y_coord, x_coord, y_coord, Compat3k.str_to_bytes(character))
    def _engage_message_formatting(self):
        self._conio_textcolor(0xF)
    #In subclasses, using e.g. WConio (binding to Windows port of conio)
    #or else implementing conio on Windows with help of ctypes
    #or using a conio extension under DOS (unlikely) etc...
    def _conio_gotoxy(self, x_coord, y_coord):
        """Move text input cursor to the coordinates (x_coord, y_coord)."""
        raise NotImplementedError
    def _conio_settitle(self, title):
        """Set window title (implementing optional)."""
        raise NotImplementedError
    def _conio_getkey(self):
        """Read a keypress."""
        raise NotImplementedError
    def _conio_puttext(self, a, b, c, d, t):
        raise NotImplementedError
    def _conio_textcolor(self, colour):
        """Change the active text colour."""
        raise NotImplementedError
