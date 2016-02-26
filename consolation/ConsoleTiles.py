from consolation.BaseTiles import BaseTiles

__copying__="""
Written by Thomas Hori

This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/."""

class ConsoleTiles(BaseTiles):
    """ A static class, subclass of BaseTiles, defining ASCII tiles.
    """
    space = " "
    vwall = "|"
    hwall = "-"
    wall_corner_nw = "-"
    wall_corner_ne = "-"
    wall_corner_sw = "-"
    wall_corner_se = "-"
    wall_TeeJnc_up = "-"
    wall_TeeJnc_dn = "-"
    wall_TeeJnc_rt = "|"
    wall_TeeJnc_lt = "|"
    wall_cross = "-"
    vfeature = ":"
    hfeature = "="
    vfeature_open = "-" #Use perpendicular wall chars, per ASCII NetHack
    hfeature_open = "|" #Use perpendicular wall chars, per ASCII NetHack
    #Levels of floor
    floor1 = "."
    floor2 = ","
    floor3 = "$"
    floor4 = "%"
    floor5 = "#"
    user = "@"
    item = "'"
    staircase = ">"
    adversary = "&"
    projectile = "*"
    wand = "/"
    #
    _error_codes = ("\xa8", "\xbf")
    _error_code = 1
