import textwrap
from consolation.Compat3k import Compat3k

__copying__="""
Written by Thomas Hori

This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/."""

class BaseDisplay(object):
    """The display interface.

    Do not create an instance directly.

    Obtain an instance using DisplaySelector.get_display().  The class
    itself is a portable interface which does not implement anything
    interface-dependant (accordingly it implements only the storage for the
    -- More -- system).  Actual functionality is obtained from platform- and
    interface-specific subclasses, a working one of which should be usable
    by calling DisplaySelector.get_backend() to get an instance.

    There is not necessarily multiple-window support, so creating multiple
    BaseDisplay is not guaranteed to work.  In particular, all existing
    implementations do not support it."""
    rpc_remote_address = None
    def __init__(self):
        self._message_queue = []
    def push_message(self, message):
        """Output a message.  This will not be displayed straight away, rather
        the full set until next user interaction will be accumulated (in what
        I previously called a "sequester") until next user interaction and
        then output with a -- More -- prompt."""
        self._message_queue.append(message)
    def slow_push_message(self, text, prefix=""):
        """Like push_message(...), but wrap to 60 chars.

        Blatantly not thread-safe.

        Optional "prefix" specifies a prefix to be added to each line
        (adds to the 60 chars)."""
        for i in textwrap.wrap(text, 60):
            self.push_message(prefix+i)
    def slow_ask_question(self, text, prefix=""):
        """Like ask_question(...), but wrap to 60 chars.

        Blatantly not thread-safe.

        May need to be overridden if questions cannot be asked in message
        area.

        Optional "prefix" specifies a prefix to be added to each line
        (adds to the 60 chars)."""
        trailer = text[len(text.rstrip()):]
        wrap = textwrap.wrap(text, 60)
        for i in wrap[:-1]:
            self.push_message(prefix+i)
        self.dump_messages() #Hopefully not needed.
        return self.ask_question(prefix+wrap[-1]+trailer)
    def interrupt(self):
        """Raises KeyboardInterrupt, for RPC use."""
        raise KeyboardInterrupt # ^c or similar pressed?
    def close_display(self): #close() seems to clash with XML-RPC library methods
        """Raises SystemExit, for RPC use."""
        self.clean()
        raise SystemExit
    #
    @staticmethod
    def works_p():
        """-->true if implementation works on this platform and environment"""
        raise NotImplementedError("should be implemented by subclass")
    def dump_messages(self, leave_hanging=0):
        """Flush messages to screen.  Normally there should be no need to use
        this as it is called automatically upon user interaction.
        
        leave_hanging is boolean, and is whether a --More-- prompt will be
        issued after the last output."""
        raise NotImplementedError("should be implemented by subclass")
    def ask_question(self, question):
        """Ask the user a question, preferably in the message area.

        Implementations should call dump_messages() first, with 
        leave_hanging as 1 or True."""
        raise NotImplementedError("should be implemented by subclass")
    def goto_point(self, x_coord, y_coord):
        """Move the user cursor/focus to coords (x_coord, y_coord)."""
        raise NotImplementedError("should be implemented by subclass")
    def set_window_title(self, title):
        """Sets the window title.  As you would expect.

        Might not be implement*able* in all cases.  If not, leave
        unimplemented.  NotImplementedError should be caught by the level
        class."""
        raise NotImplementedError("no means to set window title")
    def get_key_event(self):
        """Return a keyboard event.  Returns the entered key if it is a
        character, or one of the special values of home, up, pgup, left,
        right, end, down, pgdn, ins, del.

        Implementations should call dump_messages() first."""
        raise NotImplementedError("should be implemented by subclass")
    def get_dimensions(self):
        return (-2, -2)
    def plot_tile(self, y_coord, x_coord, tile_id):
        """Plot a tile at a point."""
        raise NotImplementedError("should be implemented by subclass")
    def plot_tile_ex(self, y_coord, x_coord, tile_id, tilechar):
        """Plot a tile at a point, suggesting a representative ASCII character."""
        raise NotImplementedError("should be implemented by subclass")
    def flush_plots(self):
        """Flush any plot caching to the screen"""
        pass
    def clean(self):
        """Clean before app closed."""
        pass
    #
    def hex_push_message(self, message):
        self.push_message(Compat3k.unhexlify(message))
    def hex_slow_push_message(self, message, prefix=""):
        self.slow_push_message(Compat3k.unhexlify(message), Compat3k.unhexlify(prefix))
    def hex_get_key_event(self):
        return Compat3k.hexlify(self.get_key_event())
    def hex_set_window_title(self, title):
        return self.set_window_title(Compat3k.unhexlify(title))
    def hex_ask_question(self, question):
        return Compat3k.hexlify(self.ask_question(Compat3k.unhexlify(question)))
    def hex_slow_ask_question(self, question, prefix=""):
        return Compat3k.hexlify(self.slow_ask_question(Compat3k.unhexlify(question), Compat3k.unhexlify(prefix)))

