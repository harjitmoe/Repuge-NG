from consolation.IbmTiles import IbmTiles

__copying__="""
Written by Thomas Hori

This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/."""

class ConioTiles(IbmTiles):
    """ A static class, subclass of IbmTiles,
    adding conio puttext colour information.
    """
    #STATIC CLASS.  NO INSTANCES.
    @classmethod #Keeps pylint happy
    def _decorate_type(cls, typ, bare):
        if typ=="wall":
            return bare+"\x04"
        elif typ=="floor":
            return bare+"\x08"
        else:
            return bare+"\x0f"
