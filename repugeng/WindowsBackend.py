import sys
from repugeng.ConsoleBackend import ConsoleBackend
from repugeng.WindowsTiles import WindowsTiles
from repugeng.compat3k import *

class WindowsBackend(ConsoleBackend):
    """Partially implementing base class"""
    _tiles_class=WindowsTiles
    def goto_point(self,x,y):
        self.point[:]=x,y
        self._conio_gotoxy(x,y)
    def set_window_title(self,title):
        self._conio_settitle(bytes(title))
    def get_key_event(self):
        self.dump_messages()
        return self._conio_getkey()
    def _plot_character(self,x,y,c):
        if not hasattr(self,"_textcolor"):
            self._textcolor=0x7
        self._conio_puttext(x,y,x,y,bytes(c+chr(self._textcolor)))
    def plot_tile(self,x,y,tile_id):
        if ("wall" in tile_id) or (tile_id in ("vfeature","hfeature")):
            self._textcolor=0x4
        elif ("floor" in tile_id):
            self._textcolor=0x8
        else:
            self._textcolor=0xF
        super(WindowsBackend,self).plot_tile(x,y,tile_id)
    def _engage_message_formatting(self):
        self._conio_textcolor(0xF)