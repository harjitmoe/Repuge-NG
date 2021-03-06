from consolation.ConsoleTiles import ConsoleTiles

__copying__="""
Written by Thomas Hori

This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/."""

class IbmTiles(ConsoleTiles):
    """ A static class, indirect subclass of BaseTiles,
    defining OEM-US tiles ("IBMGraphics").
    """
    #STATIC CLASS.  NO INSTANCES.
    vwall = "\xb3"
    hwall = "\xc4"
    wall_corner_nw = "\xda"
    wall_corner_ne = "\xbf"
    wall_corner_sw = "\xc0"
    wall_corner_se = "\xd9"
    wall_TeeJnc_up = "\xc1"
    wall_TeeJnc_dn = "\xc2"
    wall_TeeJnc_rt = "\xc3"
    wall_TeeJnc_lt = "\xb4"
    wall_cross = "\xc5"
    vfeature_open = "\xfe"
    hfeature_open = "\xfe"
    user = "\x01"
    #
    _error_code = 0
