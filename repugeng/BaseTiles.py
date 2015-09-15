from repugeng.StaticClass import StaticClass

class BaseTiles(StaticClass):
    """A static base class defining simple public and protected tileset API."""
    @classmethod #Keeps pylint happy
    def get_tile(cls, tile_id):
        """Return the tile with the given ID, or a 'huh?' tile if none.
        
        Please override _get_tile() if you must, not this one.
        """
        # Not one of Python's algorithms (see "What's New in Python 2.2"
        # for those ones) but it will do.
        bases=[cls]
        while bases:
            cls2=bases.pop(0)
            bases.extend(cls2.__bases__)
            if hasattr(cls2, "_get_tile"):
                r=cls2._get_tile(tile_id)
                if r not in cls2._error_codes:
                    return r
        return cls._error_codes[cls._error_code%len(cls._error_codes)]
    def _get_tile(cls, tile_id):
        """Return the tile with the given ID, or a 'huh?' tile if none,
        only for tiles defined here.
        """
        if hasattr(cls, tile_id):
            tilechar = getattr(cls, tile_id)
            return cls._decorate_type(cls._tile_type_wrapper(tile_id), tilechar)
        return cls._error_codes[cls._error_code%len(cls._error_codes)]
    #
    @classmethod #Keeps pylint happy
    def _tile_type_wrapper(cls, tile_id):
        """Manage cascading inheritance for _tile_type() definitions.
        
        Please do not override.
        """
        # Not one of Python's algorithms (see "What's New in Python 2.2"
        # for those ones) but it will do.
        bases=[cls]
        while bases:
            cls2=bases.pop(0)
            bases.extend(cls2.__bases__)
            if hasattr(cls2, "_tile_type"):
                r=cls2._tile_type(tile_id)
                if r!=None:
                    return r
        return None
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
