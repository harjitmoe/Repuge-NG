class GridObject(object):
    """An object which may be present on objgrid.
    
    Subclass for more functionality.
    """
    level=None
    extra=None
    tile=None #May be overridden by subclass
    tileset_expansion=None #May be overridden by subclass
    all_objects=[] #static
    pt=None
    placed=False
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
    def place(self,destx,desty):
        """Place on the specified point in the level."""
        if self.pt!=None:
            self.level.objgrid[self.pt[0]][self.pt[1]].remove(self)
        self.pt=(destx,desty)
        if len(self.level.objgrid[destx][desty]) and isinstance(self.level.objgrid[destx][desty][-1],PlayerObject):
            #Don't obscure the player
            player=self.level.objgrid[destx][desty].pop()
            self.level.objgrid[destx][desty].append(self)
            self.level.objgrid[destx][desty].append(player)
        else:
            self.level.objgrid[destx][desty].append(self)
        self.placed=True
    def lift(self):
        """Remove from the level."""
        if self.pt!=None:
            self.level.objgrid[self.pt[0]][self.pt[1]].remove(self)
            self.pt=None
        self.placed=False
    #
    __safe_for_unpickling__=True
    def __reduce__(self):
        """Implementation of the Pickle protocol."""
        return (self.__class__,(None,self.extra,self.tile))

#Cannot appear at beginning of file due to recursive importing, 
#must appear after classdef.
from repugeng.PlayerObject import PlayerObject #for isinstance(...)
