#The "threading" module over-complicates things imo
try:
    from thread import interrupt_main #pylint: disable = import-error
except ImportError:
    #3k
    from _thread import interrupt_main #pylint: disable = import-error

import time

class GridObject(object):
    """An object (animate or otherwise) which may be present on objgrid.

    Subclass for more functionality.
    """
    #
    #
    # Overridable by subclasses:
    tile = "item"
    name = "unspecified object"
    appearance = "featureless object"
    corpse_type = None
    vitality = 0 #Hit-points, enchantment level... depending on object
    maxhp = 9999
    init_hp_interval = 0
    #
    #
    # Not overridable by subclasses:
    level = None
    extra = None #Haven't the foggiest anymore...
    all_objects = [] #class attribute, as assigned to mutable here
    pt = None
    status = "unplaced" #unplaced, placed, contained or defunct
    container = None #i.e. the one containing the object
    handlers = None
    known = None
    myinterface = None
    priority = 0
    contents = None
    #
    #
    # Initialisation
    def __init__(self, game, extra=None, tile=-1, play=0):
        """Overriding is not recommended unless __reduce__ also
        overridden

        Argument play is true if should attach new interface."""
        self.game = game
        self.extra = extra
        if tile != -1:
            self.tile = tile
        GridObject.all_objects.append(self)
        self.handlers = []
        self.known = []
        if play:
            self.play()
        #Two underscores, mangles to _PlayableObject__playercheck
        self.add_handler(1, self.__playercheck)
        self.add_handler(self.init_hp_interval, self.up_hitpoint)
        self.contents = []
        self.initialise()
    def initialise(self):
        """Just been spawned.  Do what?  Hook for subclasses."""
        pass
    #
    #
    # Connecting interfaces (possession) and disconnecting interfaces
    def play(self, myinterface=None):
        """Connect to player."""
        if myinterface == None:
            myinterface = self.game.InterfaceClass(self, use_rpc=self.game.use_rpc)
        self.myinterface = myinterface
    def unplay(self):
        """Disconnect from player."""
        self.myinterface = None
    #
    #
    # The handler registration / execution system
    def tick(self):
        """Your move.  If you are a creature, move!

        Calls handlers."""
        for every, handler, n in self.handlers:
            if not n[0]:
                handler()
            n[0] = (n[0]+1)%every
    def add_handler(self, gap, boundmethod):
        """Add a tick handler.

        Gap (>0) is how many ticks between pauses."""
        assert gap >= 0
        if gap: #gap==0 means "don't add"
            self.handlers.append((gap, boundmethod, [0]))
    def remove_handler(self, handlerbm):
        """Remove a tick handler."""
        for i, (every, handler, n) in enumerate(self.handlers[:]): #pylint: disable = unused-variable
            if handler == handlerbm:
                del self.handlers[i]
    #
    #
    # Handling user input when applicable
    def conv_to_target(self, e):
        #Note: this function is old.
        if e not in ("down", "up", "left", "right", "8", "4", "6", "2", "7", "9",
                     "1", "3", "h", "j", "k", "l", "y", "u", "b", "n"):
            return None
        if e in ("left", "4", "h"):
            target = (self.pt[0]-1, self.pt[1])
        if e in ("down", "2", "j"):
            target = (self.pt[0], self.pt[1]+1)
        if e in ("up", "8", "k"):
            target = (self.pt[0], self.pt[1]-1)
        if e in ("right", "6", "l"):
            target = (self.pt[0]+1, self.pt[1])
        if e in ("7", "y"):
            target = (self.pt[0]-1, self.pt[1]-1)
        if e in ("9", "u"):
            target = (self.pt[0]+1, self.pt[1]-1)
        if e in ("1", "b"):
            target = (self.pt[0]-1, self.pt[1]+1)
        if e in ("3", "n"):
            target = (self.pt[0]+1, self.pt[1]+1)
        return target
    def __playercheck(self): #Two underscores, mangles to _GridObject__playercheck
        if self.myinterface == None:
            return
        if self.level == None:
            return
        if self.vitality <= 0:
            self.die()
            return
        self.level.redraw()
        if self.status != "placed":
            return
        if len(self.level.child_interfaces) > 1:
            self.myinterface.push_message("Your turn.")
        e = self.myinterface.get_key_event()
        if e in ("\x03", "\x04", "\x1a"): #ETX ^C, EOT ^D, and ^Z
            #Does not go through to Python otherwise, meaning that Linux main terminals
            #are rendered otherwise out of order until someone kills Collecto
            #from a different terminal or over SSH (or rlogin).
            #This is relevant if someone is running this on an RPi.
            raise KeyboardInterrupt #^c, ^d or ^z pressed
        elif e in ("down", "up", "left", "right", "8", "4", "6", "2", "7", "9",
                   "1", "3", "h", "j", "k", "l", "y", "u", "b", "n"):
            target = self.conv_to_target(e)
            if self.game.debug_ghost or self.level.handle_move(target, self):
                self.place(*target)
        elif e == "#":
            name = "#"+self.myinterface.ask_question("#")
            if name in ("#debug", "#debugon"):
                self.game.debug = 1
            elif self.game.debug:
                if name in ("#debugoff",):
                    self.game.debug = 0
                elif name in ("#ghost", "#ghoston"):
                    self.game.debug_ghost = 1
                elif name in ("#ghostoff",):
                    self.game.debug_ghost = 0
                elif name in ("#fovoff", "#fovoffon", "#clairvoyant",
                              "#allsight", "#seeall"):
                    self.game.debug_fov_off = 1
                elif name in ("#fov", "#fovon", "#fovoffoff", "#clairvoyantoff",
                              "#allsightoff", "#seealloff"):
                    self.game.debug_fov_off = 0
                elif name.startswith("#passthrough "):
                    self.game.handle_command(name.split(" ", 1)[1], self)
                elif name in ("#bugreport", "#report", "#gurumeditation", "#guru"):
                    self.game.dump_report()
                elif name in ("#testerror",):
                    raise RuntimeError("testing error handler")
                elif name in ("#abort", "#abrt", "#kill"):
                    import os
                    os.abort()
                elif name in ("#quit",):
                    interrupt_main()
                else:
                    self.level.handle_command(name, self)
            else:
                self.level.handle_command(name, self)
        else:
            self.level.handle_command(e, self)
        if len(self.level.child_interfaces) > 1:
            self.myinterface.push_message("Turn over.")
            self.myinterface.dump_messages()
    def up_hitpoint(self):
        if self.vitality < self.maxhp:
            self.vitality += 1
    #
    #
    # Moving, removing and changing
    def place(self, destx, desty, newlevel=None):
        """Place on the specified point in the level, lifting from previous point."""
        if self.status == "contained":
            self.container.remove(self)
        oldlevel = self.level
        if newlevel == None:
            newlevel = oldlevel
        if self.pt != None and oldlevel != None:
            if self in oldlevel.objgrid[self.pt[0]][self.pt[1]]:
                self.lift()
        self.pt = (destx, desty)
        self.level_rebase(newlevel)
        self.level.child_objects.append(self)
        if len(newlevel.objgrid[destx][desty]) \
           and hasattr(newlevel.objgrid[destx][desty][-1], "myinterface") \
           and newlevel.objgrid[destx][desty][-1].myinterface != None:
            #Don't obscure the player
            player = newlevel.objgrid[destx][desty].pop()
            newlevel.objgrid[destx][desty].append(self)
            newlevel.objgrid[destx][desty].append(player)
        else:
            newlevel.objgrid[destx][desty].append(self)
        self.status = "placed"
        newlevel.redraw()
    def level_rebase(self, newlevel):
        """Re-associate with a different level.

        Subclasses may need to override this to take additional action here."""
        if self.status == "placed":
            self.lift()
        # DO NOT REMOVE IT FROM ITS CONTAINER here
        # This method is propagated from containers to their contents below.
        if self.level:
            assert self not in self.level.child_objects
        self.level = newlevel
        for i in self.contents:
            i.level_rebase(newlevel)
        if self.myinterface != None:
            self.myinterface.level_rebase(newlevel)
    def lift(self):
        """Remove from the level."""
        if self.pt != None:
            self.level.child_objects.remove(self)
            assert self not in self.level.child_objects
            self.level.objgrid[self.pt[0]][self.pt[1]].remove(self)
            self.level = None
            self.pt = None
        else:
            assert self not in self.level.child_objects
        self.status = "unplaced"
    def leave_corpse_p(self):
        """--> True to leave a corpse or False not to.

        Default just returns True."""
        return True
    def die(self):
        if self.myinterface != None:
            self.myinterface.ask_question("DYWYPI?")
            self.myinterface.close()
        if self.corpse_type:
            if self.leave_corpse_p():
                self.polymorph(self.corpse_type)
                return
        self.lift()
        GridObject.all_objects.remove(self)
        self.level = None
        self.status = "defunct"
    def polymorph(self, otype):
        """Note that this object becomes defunct and a new one is made/returned.

        Obviously the type passed for the new one must be a GridObject subtype."""
        if not issubclass(otype, GridObject):
            raise TypeError("you cannot play as that! (not a GridObject subclass)")
        novus = otype(self.game, self.extra, play=0)
        #
        if self.myinterface != None:
            novus.play(self.myinterface)
        novus.known = self.known
        novus.contents = self.contents
        novus.vitality = (self.vitality if self.vitality > novus.maxhp else novus.maxhp)
        #
        if self.status == "contained":
            self.container.insert(novus)
            self.container.remove(self)
        elif self.status == "placed":
            novus.place(*self.pt+(self.level,))
            self.lift()
        GridObject.all_objects.remove(self)
        if self.myinterface != None:
            self.myinterface.playerobj = novus
        self.level = None
        self.status = "defunct"
        return novus
    def throw(self, direction, startpt, level):
        self.place(startpt[0], startpt[1], level)
        _w, _h = self.level.grid_dimens()
        lp=0
        while 1:
            lp+=1
            if lp>(_w*_h):
                raise ValueError("infinite tightloop %s %s"%(startpt,self.pt))
            #Given that it is not None, we gather that it is coords
            x, y = self.pt #pylint: disable = unpacking-non-sequence
            adjacents = ([(x-1, y-1)] if x > 0 and y > 0 else []) \
                      + ([(x, y-1)] if y > 0 else []) \
                      + ([(x+1, y-1)] if x < (_w-1) and y > 0 else []) \
                      + ([(x+1, y)] if x < (_w-1) else []) \
                      + ([(x+1, y+1)] if x < (_w-1) and y < (_h-1) else []) \
                      + ([(x, y+1)] if y < (_h-1) else []) \
                      + ([(x-1, y+1)] if x > 0 and y < (_h-1) else []) \
                      + ([(x-1, y)] if x > 0 else [])
            if direction=="NW":
                target=(x-1,y-1)
            elif direction=="N":
                target=(x,y-1)
            elif direction=="NE":
                target=(x+1,y-1)
            elif direction=="E":
                target=(x+1,y)
            elif direction=="SE":
                target=(x+1,y+1)
            elif direction=="S":
                target=(x,y+1)
            elif direction=="SW":
                target=(x-1,y+1)
            elif direction=="W":
                target=(x-1,y)
            if target not in adjacents:
                break
            #
            try: #XXX kludge/fragile/assumes
                floorlevel = type(0)(self.level.get_index_grid(*self.pt)[0][5:])
            except ValueError:
                floorlevel = 1 #Needed or mazed subclass breaks
            nxtstat = self.level.get_index_grid(*target)[0]
            if self.level.objgrid[target[0]][target[1]]:
                for obj in self.level.objgrid[target[0]][target[1]][:]:
                    if hasattr(obj, "myinterface") and obj.myinterface != None:
                        self.hit(obj)
                        self.place(*target)
                        return
            if nxtstat.startswith("floor"):
                newlevel = type(0)(nxtstat[5:])
                if (newlevel-floorlevel) <= 1:
                    self.place(*target)
                    self.level.redraw()
                    time.sleep(0.05)
            else:
                break
        self.level.redraw()
    def hit(self, obj):
        if type(self) in obj.known: #pylint: disable = unidiomatic-typecheck
            obj.myinterface.push_message("The %s hits!"%self.name)
        else:
            obj.myinterface.push_message("The %s hits!"%self.appearance)
        obj.vitality -= 1
    #
    #
    # Support for functioning as a container
    def empty(self):
        return not self.contents
    def insert(self, obj):
        if obj.status == "placed":
            obj.lift()
        elif obj.status == "contained":
            obj.container.remove(obj)
        elif obj.status != "unplaced":
            raise ValueError("unheard-of obj status %r"%obj.status)
        #
        if obj in self.contents:
            raise RuntimeError("unplaced obj in container's inventory")
        self.contents.append(obj)
        obj.status = "contained"
        obj.container = self
    def remove(self, obj):
        self.contents.remove(obj)
        obj.status = "unplaced"
        obj.container = None
    def drop(self, obj, pt):
        self.remove(obj)
        obj.place(*pt)
    def dump(self, pt):
        for obj in self.contents[:]:
            self.drop(obj, pt)
    def __iter__(self):
        return iter(self.contents)
    #
    __safe_for_unpickling__ = True
    def __reduce__(self):
        """Implementation of the Pickle protocol."""
        return (self.__class__, (None, self.extra, self.tile))
