class GridObject(object):
    """An object which may be present on objgrid.
    
    Subclass for more functionality.
    """
    level=None
    extra=None
    tile=None #May be overridden by subclass
    tileset_expansion=None #May be overridden by subclass
    all_objects=[] #static
    def __init__(self,level,extra=None,tile=-1):
        """Overriding is not recommended unless __reduce__ also
        overridden"""
        self.level=level
        self.extra=extra
        if tile!=-1:
            self.tile=tile
        if self.tileset_expansion:
            self.level.backend.attach_expansion_pack(self.tileset_expansion)
        GridObject.all_objects.append(self)
    def tick(self):
        """Your move.  If you are a creature, move!
        
        Do override if appropriate.  Default is nothing."""
        pass
    def destroy(self):
        GridObject.all_objects.remove(self)
        self.level=None
        self.extra=None
        self.tile=None
    #
    __safe_for_unpickling__=True
    def __reduce__(self):
        """Implementation of the Pickle protocol."""
        return (self.__class__,(None,self.extra,self.tile))
