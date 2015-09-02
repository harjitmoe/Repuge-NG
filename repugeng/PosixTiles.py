from repugeng.ConsoleTiles import ConsoleTiles
class PosixTiles(ConsoleTiles):
    #STATIC CLASS.  NO INSTANCES.
    @classmethod
    def _decorate_wall(cls, bare):
        return "\x1b[1;31m"+bare
    @classmethod
    def _decorate_floor(cls, bare):
        return "\x1b[1;30m"+bare
    @classmethod
    def _decorate_regular(cls, bare):
        return "\x1b[22;37m"+bare
