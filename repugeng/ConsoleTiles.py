from repugeng.StaticClass import StaticClass

class ConsoleTiles(StaticClass):
    def get_bare_tile_character(cls, tile_id):
        error_codes = ("\xa8", "\xbf")
        if hasattr(cls, tile_id):
            return getattr(cls, tile_id)
        if hasattr(super(cls), "get_tile_character"):
            return super(cls).get_bare_tile_character(tile_id)
        return error_codes[cls._error_code%len(error_codes)]
    def get_tile_character(cls, tile_id):
        if ("wall" in tile_id) or (tile_id in ("vfeature", "hfeature")):
            return cls._decorate_wall(cls.get_bare_tile_character(tile_id))
        elif "floor" in tile_id:
            return cls._decorate_floor(cls.get_bare_tile_character(tile_id))
        else:
            return cls._decorate_regular(cls.get_bare_tile_character(tile_id))
    def attach_expansion_pack(cls, cls2):
        pass
    #
    def _decorate_wall(cls, bare):
        return bare
    def _decorate_floor(cls, bare):
        return bare
    def _decorate_regular(cls, bare):
        return bare
    #
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
    _error_code = 1
    expansion_packs = []

