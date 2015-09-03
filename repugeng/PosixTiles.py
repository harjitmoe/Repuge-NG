from repugeng.ConsoleTiles import ConsoleTiles
class PosixTiles(ConsoleTiles):
    """ A static class, subclass of ConsoleTiles,
    adding ANSI-escape colouring.
    """
    #STATIC CLASS.  NO INSTANCES.
    @classmethod #Keeps pylint happy
    def _decorate_wall(cls, bare):
        return "\x1b[1;31m"+bare
    @classmethod #Keeps pylint happy
    def _decorate_floor(cls, bare):
        return "\x1b[1;30m"+bare
    @classmethod #Keeps pylint happy
    def _decorate_regular(cls, bare):
        return "\x1b[22;37m"+bare
