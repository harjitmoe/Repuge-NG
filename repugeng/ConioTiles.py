from repugeng.ConsoleTiles import ConsoleTiles
class ConioTiles(ConsoleTiles):
    #STATIC CLASS.  NO INSTANCES.
    @classmethod
    def _decorate_wall(cls, bare):
        return bare+"\x04"
    @classmethod
    def _decorate_floor(cls, bare):
        return bare+"\x08"
    @classmethod
    def _decorate_regular(cls, bare):
        return bare+"\x0f"
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
