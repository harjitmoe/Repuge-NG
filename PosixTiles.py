from ConsoleTiles import ConsoleTiles
class PosixTiles(ConsoleTiles):
    #STATIC CLASS.  NO INSTANCES.
    @staticmethod
    def get_tile_character(tile_id):
        if ("wall" in tile_id) or (tile_id in ("vfeature","hfeature")):
            return "\x1b[1;31m"+ConsoleTiles.get_tile_character(tile_id)
        elif ("floor" in tile_id):
            return "\x1b[1;30m"+ConsoleTiles.get_tile_character(tile_id)
        else:
            return "\x1b[22;37m"+ConsoleTiles.get_tile_character(tile_id)

