from repugeng.IbmTiles import IbmTiles
class ConioTiles(IbmTiles):
    """ A static class, subclass of IbmTiles,
    adding conio puttext colour information.
    """
    #STATIC CLASS.  NO INSTANCES.
    @classmethod #Keeps pylint happy
    def _decorate_type(cls, type, bare):
        if type=="wall":
            return bare+"\x04"
        elif type=="floor":
            return bare+"\x08"
        else:
            return bare+"\x0f"
