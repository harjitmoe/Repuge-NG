from repugeng.BaseTiles import BaseTiles

class ConsoleTiles(BaseTiles):
    """ A static class, subclass of BaseTiles, defining ASCII tiles.
    """
    space = " "
    vwall = "|"
    hwall = "-"
    wall_corner_nw = "-" #In true Rogue style
    wall_corner_ne = "-" #In true Rogue style
    wall_corner_sw = "-" #In true Rogue style
    wall_corner_se = "-" #In true Rogue style
    wall_TeeJnc_up = "-" #In true continuation of Rogue style
    wall_TeeJnc_dn = "-" #In true continuation of Rogue style
    wall_TeeJnc_rt = "|" #In true continuation of Rogue style
    wall_TeeJnc_lt = "|" #In true continuation of Rogue style
    wall_cross = "-" #In true continuation of Rogue style
    vfeature = ":"
    hfeature = "="
    vfeature_open = "-" #Use perpendicular wall chars, per ASCII NetHack
    hfeature_open = "|" #Use perpendicular wall chars, per ASCII NetHack
    #Levels of floor
    floor1 = "."
    floor2 = ","
    floor3 = "/"
    floor4 = "$"
    floor5 = "#"
    user = "@"
    item = "'"
    staircase = ">"
    adversary = "&"
    #
    _error_codes = ("\xa8", "\xbf")
    _error_code = 1
