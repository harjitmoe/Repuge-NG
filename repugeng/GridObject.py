class GridObject(object):
    """An object (animate or otherwise) which may be present on objgrid.
    
    Subclass for more functionality.
    """
    level=None
    extra=None #Haven't the foggiest anymore...
    tile="item" #May be overridden by subclass
    tileset_expansion=None #May be overridden by subclass
    corpse_type=None #May be overridden by subclass
    all_objects=[] #static attribute
    pt=None
    status="unplaced" #unplaced, placed, contained or defunct
    container=None #i.e. the one containing the object
    handlers=None
    inventory=None #A Container instance or None
    vitality=0 #Hit-points, enchantment level... depending on object
    maxhp=9999
    name="unspecified object"
    appearance="featureless object"
    def __init__(self,game,extra=None,tile=-1,play=0):
        """Overriding is not recommended unless __reduce__ also
        overridden
        
        Argument play is true if should attach new interface.
        See PlayableObject."""
        self.game=game
        self.extra=extra
        if tile!=-1:
            self.tile=tile
        if self.tileset_expansion:
            game.playerobj.interface.backend.attach_expansion_pack(self.tileset_expansion)
        GridObject.all_objects.append(self)
        self.handlers=[]
        self.initialise(play)
    def initialise(self,play=None):
        """Just been spawned.  Do what?
        
        Argument play is true if should attach new interface."""
        pass
    def tick(self):
        """Your move.  If you are a creature, move!
        
        Calls handlers."""
        for every,handler,n in self.handlers:
            if not n[0]:
                handler()
            n[0]=(n[0]+1)%every
    def add_handler(self,gap,boundmethod):
        """Add a tick handler.  
        
        Gap (>0) is how many ticks between pauses."""
        assert gap>0
        self.handlers.append((gap,boundmethod,[0]))
    def remove_handler(self,handlerbm):
        """Remove a tick handler."""
        assert gap>0
        for i,(every,handler,n) in enumerate(self.handlers[:]):
            if boundmethod==handlerbm:
                del self.handlers[i]
    def place(self,destx,desty,newlevel=None):
        """Place on the specified point in the level, lifting from previous point."""
        oldlevel=self.level
        if newlevel==None:
            newlevel=oldlevel
        if self.pt!=None and oldlevel!=None:
            oldlevel.objgrid[self.pt[0]][self.pt[1]].remove(self)
        self.pt=(destx,desty)
        self.level_rebase(newlevel)
        if len(newlevel.objgrid[destx][desty]) and hasattr(newlevel.objgrid[destx][desty][-1],"interface") and newlevel.objgrid[destx][desty][-1].interface!=None:
            #Don't obscure the player
            player=newlevel.objgrid[destx][desty].pop()
            newlevel.objgrid[destx][desty].append(self)
            newlevel.objgrid[destx][desty].append(player)
        else:
            newlevel.objgrid[destx][desty].append(self)
        self.status="placed"
    def level_rebase(self,newlevel):
        """Re-associate with a different level.
        
        Subclasses may need to override this to take additional action here."""
        self.level=newlevel
        if self.inventory!=None:
            self.inventory.level_rebase(newlevel)
    def lift(self):
        """Remove from the level."""
        if self.pt!=None:
            self.level.objgrid[self.pt[0]][self.pt[1]].remove(self)
            self.level=None
            self.pt=None
        self.status="unplaced"
    def leave_corpse_p(self):
        """--> True to leave a corpse or False not to.  
        
        Default just returns True."""
        return True
    def die(self):
        if self.corpse_type:
            if self.leave_corpse_p():
                self.polymorph(self.corpse_type)
                return
        if self.inventory!=None:
            self.inventory.dump(self.pt)
            self.inventory.die()
        self.lift()
        GridObject.all_objects.remove(self)
        self.level=None
        self.status="defunct"
    def polymorph(self,otype):
        """Note that this object becomes defunct and a new one made."""
        new=otype(self.level,self.extra,play=0)
        if self.inventory!=None:
            if new.inventory!=None:
                new.inventory.die()
                new.inventory=self.inventory
            else:
                self.inventory.dump(self.pt)
                self.inventory.die()
        if self.status=="contained":
            self.container.insert(new)
            self.container.remove(self)
        elif self.status=="placed":
            new.place(*self.pt)
            self.lift()
        new.vitality=self.vitality
        GridObject.all_objects.remove(self)
        self.level=None
        self.status="defunct"
    #
    __safe_for_unpickling__=True
    def __reduce__(self):
        """Implementation of the Pickle protocol."""
        return (self.__class__,(None,self.extra,self.tile))
