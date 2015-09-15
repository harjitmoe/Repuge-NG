from repugeng.StaticClass import StaticClass

class BaseTiles(StaticClass):
    """A static base class defining simple public and protected tileset API."""
    @classmethod #Keeps pylint happy
    def get_tile(cls, tile_id):
        """Return the tile with the given ID, or a 'huh?' tile if none.
        
        Please override _get_tile() if you must, not this one.
        """
        r=cls._cascade_method("_get_tile", cls._error_codes, tile_id)
        if r in cls._error_codes:
            return cls._error_codes[cls._error_code%len(cls._error_codes)]
        return r
    def _get_tile(cls, tile_id):
        """Return the tile with the given ID, or a 'huh?' tile if none,
        only for tiles defined here.
        """
        if hasattr(cls, tile_id):
            tilechar = getattr(cls, tile_id)
            return cls._decorate_type(cls._cascade_method("_tile_type", (None,), tile_id), tilechar)
        return cls._error_codes[cls._error_code%len(cls._error_codes)]
    #
    def _tile_type(cls, tile_id):
        """Determine the tile type for decoration purposes."""
        if ("wall" in tile_id) or (tile_id in ("vfeature", "hfeature")):
            return "wall"
        elif "floor" in tile_id:
            return "floor"
        else:
            return None
    @classmethod #Keeps pylint happy
    def _decorate_type(cls, typ, bare):
        """Decorate a wall tile."""
        return bare
    #
    _error_codes = [None]
    _error_code = 0
