from repugeng.ConsoleTiles import ConsoleTiles
class PosixTiles(ConsoleTiles):
    """ A static class, subclass of ConsoleTiles,
    adding ANSI-escape colouring.
    """
    #STATIC CLASS.  NO INSTANCES.
    @classmethod #Keeps pylint happy
    def _decorate_type(cls, type, bare):
        if type=="wall":
            return "\x1b[1;31m"+bare
        elif type=="floor":
            return "\x1b[1;30m"+bare
        else:
            return "\x1b[22;37m"+bare
