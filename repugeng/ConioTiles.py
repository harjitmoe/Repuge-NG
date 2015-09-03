from repugeng.IbmTiles import IbmTiles
class ConioTiles(IbmTiles):
    """ A static class, subclass of ConsoleTiles,
    adding conio puttext colour information.
    """
    #STATIC CLASS.  NO INSTANCES.
    @classmethod #Keeps pylint happy
    def _decorate_wall(cls, bare):
        return bare+"\x04"
    @classmethod #Keeps pylint happy
    def _decorate_floor(cls, bare):
        return bare+"\x08"
    @classmethod #Keeps pylint happy
    def _decorate_regular(cls, bare):
        return bare+"\x0f"
