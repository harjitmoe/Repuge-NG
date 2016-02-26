from consolation.StaticClass import StaticClass

__copying__="""
Written by Thomas Hori

This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/."""

class BaseTiles(StaticClass):
    """A static base class defining simple public and protected tileset API."""
    @classmethod #Keeps pylint happy
    def get_tile(cls, tile_id, default=None):
        """Return the tile with the given ID, or a 'huh?' tile if none.
        
        Please override _get_tile() if you must, not this one.
        """
        r = cls._cascade_method("_get_tile", tile_id)
        if r == None:
            if default != None:
                return cls._decorate_type(cls._cascade_method("_tile_type", tile_id), default)
            return cls._decorate_type("error", cls._error_codes[cls._error_code%len(cls._error_codes)])
        return r
    @classmethod #Keeps pylint happy
    def _get_tile(cls, tile_id):
        """Return the tile with the given ID, or None if none,
        only for tiles defined here.
        """
        if hasattr(cls, tile_id):
            tilechar = getattr(cls, tile_id)
            return cls._decorate_type(cls._cascade_method("_tile_type", tile_id), tilechar)
        return None
    #
    @classmethod #Keeps pylint happy
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
