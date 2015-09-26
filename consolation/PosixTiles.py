from consolation.ConsoleTiles import ConsoleTiles

__copying__="""
This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/."""

class PosixTiles(ConsoleTiles):
    """ A static class, subclass of ConsoleTiles,
    adding ANSI-escape colouring.
    """
    #STATIC CLASS.  NO INSTANCES.
    @classmethod #Keeps pylint happy
    def _decorate_type(cls, typ, bare):
        if typ=="wall":
            return "\x1b[1;31m"+bare
        elif typ=="floor":
            return "\x1b[1;30m"+bare
        else:
            return "\x1b[22;37m"+bare
