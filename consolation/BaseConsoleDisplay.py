import sys
from consolation.BaseDisplay import BaseDisplay
from consolation.ConsoleTiles import ConsoleTiles
from consolation.Compat3k import Compat3k
try:
    import thread
except ImportError:
    import _thread as thread

__copying__="""
Written by Thomas Hori

This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/."""

class BaseConsoleDisplay(BaseDisplay):
    """An base class implementing parts of the Display API
    in terms of an abstract terminal interface.
    """
    _tiles_class = ConsoleTiles
    def __init__(self, *a, **kw):
        self.point = [0, 0]
        self.mylock=thread.allocate_lock()
        super(BaseConsoleDisplay, self).__init__(*a, **kw)
    def _output_text(self, i):
        sys.stderr.write(i)
        sys.stderr.flush() #breaks on 3.1 on win32 otherwise
    def _engage_message_formatting(self):
        pass
    def _end_message_formatting(self):
        pass
    def clean(self):
        self._reset_terminal()
    def _reset_terminal(self):
        pass #Subclasses to only implement if actually needed
    def dump_messages(self, leave_hanging=0):
        if not leave_hanging:
            if self._message_queue:
                while self._message_queue[1:]:
                    line = self._message_queue.pop(0)
                    self._put_to_message_area(line+" -- More -- ", 1)
                self._put_to_message_area(self._message_queue.pop(), 0)
        else:
            while self._message_queue:
                line = self._message_queue.pop(0)
                self._put_to_message_area(line+" -- More -- ", 1)
    def ask_question(self, question):
        self.dump_messages(1)
        return self._put_to_message_area(question, 1)
    def plot_tile(self, x_coord, y_coord, tile_id):
        return self._plot_character(y_coord, x_coord, self._tiles_class.get_tile(tile_id))
    def plot_tile_ex(self, x_coord, y_coord, tile_id, tilechar):
        return self._plot_character(y_coord, x_coord, self._tiles_class.get_tile(tile_id, tilechar))
    #
    def _plot_character(self, y_coord, x_coord, character):
        raise NotImplementedError("should be implemented by subclass")
    def _put_to_message_area(self, s, ask):
        """The backend behind all putting to the console message area,
        for ask or say.

        Not thread safe.

        Arguments:
        - s: The string to output.
        - ask: Boolean, should user input be waited for?
        - collect_input: Boolean, should the user input be collected?  Keep as 1
          unless the user is supposed to acknowledge receipt of the message with
          Return but not actually supposed to input stuff (e.g. More prompt).
        """
        _w = self.get_dimensions()[0]
        if _w < 0:
            _w = 80
        s_padded = s
        if len(s) < (_w-1):
            s_padded += (_w-len(s)-1)*" "
        self._engage_message_formatting()
        save_point = self.point[:]
        retu = None
        self.goto_point(0,21)
        self._output_text(s_padded)
        if ask:
            self._reset_terminal()
            retu = Compat3k.prompt_user("\r"+s)
        self._end_message_formatting()
        self.goto_point(*save_point)
        return retu

