class GridObject(object):
    """An object which may be present on objgrid.
    
    Subclass for more functionality.
    """
    level=None
    extra=None
    tile=None #May be overridden by subclass
    def __init__(self,level,extra=None,tile=-1):
        """Overriding is not recommended unless __reduce__ also
        overridden"""
        self.level=level
        self.extra=extra
        if tile!=-1:
            self.tile=tile
    def tick(self):
        """Your move.  If you are a creature, move!
        
        Do override if appropriate.  Default is nothing."""
        pass
    #
    __safe_for_unpickling__=True
    def __reduce__(self):
        """Implementation of the Pickle protocol."""
        return (self.__class__,(None,self.extra,self.tile))
