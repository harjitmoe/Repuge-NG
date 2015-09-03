from repugeng.StaticClass import StaticClass

class BaseTiles(StaticClass):
    """A static base class defining simple public and protected tileset API."""
    @classmethod #Keeps pylint happy
    def get_tile(cls, tile_id):
        """Return the tile with the given ID, or a 'huh?' tile on error."""
        if hasattr(cls, tile_id):
            tilechar = getattr(cls, tile_id)
            if ("wall" in tile_id) or (tile_id in ("vfeature", "hfeature")):
                return cls._decorate_wall(tilechar)
            elif "floor" in tile_id:
                return cls._decorate_floor(tilechar)
            else:
                return cls._decorate_regular(tilechar)
        if hasattr(super(cls), "get_tile"):
            return super(cls).get_tile(tile_id)
        return cls._error_codes[cls._error_code%len(cls._error_codes)]
    #
    @classmethod #Keeps pylint happy
    def _decorate_wall(cls, bare):
        """Decorate a wall tile."""
        return bare
    @classmethod #Keeps pylint happy
    def _decorate_floor(cls, bare):
        """Decorate a floor tile."""
        return bare
    @classmethod #Keeps pylint happy
    def _decorate_regular(cls, bare):
        """Decorate a tile which is neither wall nor floor."""
        return bare
    #
    _error_codes = [None]
    _error_code = 0
