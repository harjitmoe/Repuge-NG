from repugeng.ConsoleBackend import ConsoleBackend
from repugeng.WindowsTiles import WindowsTiles
from repugeng.compat3k import * #pylint: disable = redefined-builtin, wildcard-import, unused-wildcard-import

class WindowsBackend(ConsoleBackend):
    """Partially implementing base class"""
    _tiles_class = WindowsTiles
    _textcolor = None
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
        if not hasattr(self, "_textcolor"):
            self._textcolor = 0x7
        self._conio_puttext(x, y, x, y, bytes(c+chr(self._textcolor)))
    def plot_tile(self, x, y, tile_id):
        if ("wall" in tile_id) or (tile_id in ("vfeature", "hfeature")):
            self._textcolor = 0x4
        elif "floor" in tile_id:
            self._textcolor = 0x8
        else:
            self._textcolor = 0xF
        super(WindowsBackend, self).plot_tile(x, y, tile_id)
    def _engage_message_formatting(self):
        self._conio_textcolor(0xF)
    #In subclasses, using e.g. WConio (binding to Windows port of conio)
    #or else implementing conio with help of ctypes etc...
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
