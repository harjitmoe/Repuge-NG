from repugeng.GridObject import GridObject
from repugeng.Container import Container

class PlayableObject(GridObject):
    """A grid object with ability to be controlled by a player.
    """
    tile="user"
    vitality=10
    known=None
    maxhp=10
    init_hp_interval=5
    name="playable object"
    appearance="playable object"
    interface=None
    def initialise(self,play):
        """Just been spawned.  Do what?
        
        Argument play is true if should attach new interface."""
        if play:
            self.play()
        self.inventory=Container(self.level)
        self.known=[]
        self.add_handler(1,self._PlayableObject__playercheck)
        self.add_handler(self.init_hp_interval,self.up_hitpoint)
        self.initialise_playable()
    def initialise_playable(self):
        """Just been spawned and set up as a playable.  Do what?"""
        pass
    def play(self,interface=None):
        """Connect to player."""
        if interface==None:
            interface=self.level.InterfaceClass(self)
        self.interface=interface
    def unplay(self):
        """Disconnect from player."""
        self.interface=None
    def _PlayableObject__playercheck(self): #Two underscores
        if self.interface==None:
            return
        if self.vitality<=0:
            self.die()
            return
        self.interface.redraw()
        if self.status!="placed":
            return
        e=self.interface.backend.get_key_event()
        if e in ("\x03","\x04","\x1a"): #ETX ^C, EOT ^D, and ^Z
            #Does not go through to Python otherwise, meaning that Linux main terminals
            #are rendered otherwise out of order until someone kills Collecto
            #from a different terminal or over SSH (or rlogin).
            #This is relevant if someone is running this on an RPi.
            raise KeyboardInterrupt #^c, ^d or ^z pressed
        elif e in ("down","up","left","right","8","4","6","2","7","9","1","3","h","j","k","l","y","u","b","n"):
            if e in ("left", "4","h"): target=(self.pt[0]-1,self.pt[1])
            if e in ("down", "2","j"): target=(self.pt[0],self.pt[1]+1)
            if e in ("up",   "8","k"): target=(self.pt[0],self.pt[1]-1)
            if e in ("right","6","l"): target=(self.pt[0]+1,self.pt[1])
            if e in ("7","y"): target=(self.pt[0]-1,self.pt[1]-1)
            if e in ("9","u"): target=(self.pt[0]+1,self.pt[1]-1)
            if e in ("1","b"): target=(self.pt[0]-1,self.pt[1]+1)
            if e in ("3","n"): target=(self.pt[0]+1,self.pt[1]+1)
            if self.level.debug_ghost or self.level.handle_move(target,self):
                self.place(*target)
        elif e=="#":
            name="#"+self.interface.backend.ask_question("#")
            if name in ("#debug","#debugon"):
                self.level.debug=1
            elif self.level.debug:
                if name=="#debugoff":
                    self.level.debug=0
                elif name in ("#ghost","#ghoston"):
                    self.level.debug_ghost=1
                elif name=="#ghostoff":
                    self.level.debug_ghost=0
                elif name in ("#fovoff","#fovoffon","#clairvoyant","#allsight","#seeall"):
                    self.level.debug_fov_off=1
                elif name in ("#fov","#fovon","#fovoffoff","#clairvoyantoff","#allsightoff","#seealloff"):
                    self.level.debug_fov_off=0
                elif name.startswith("#passthrough "):
                    self.level.handle_command(name.split(" ",1)[1],self)
                elif name in ("#bugreport","#report","#gurumeditation","#guru"):
                    self.level._dump_report()
                elif name in ("#testerror"):
                    raise RuntimeError("testing error handler")
                elif name in ("#abort","#abrt","#kill"):
                    import os
                    os.abort()
                elif name in ("#quit"):
                    import sys
                    sys.exit()
                else:
                    self.level.handle_command(name,self)
            else:
                self.level.handle_command(name,self)
        else:
            self.level.handle_command(e,self)
    def up_hitpoint(self):
        if self.vitality<self.maxhp:
            self.vitality+=1
    def level_rebase(self,newlevel):
        GridObject.level_rebase(self,newlevel)
        if self.interface!=None:
            self.interface.level_rebase(newlevel)
    def die(self):
        if self.interface!=None:
            self.interface.backend.ask_question("DYWYPI?")
            self.interface.close()
        GridObject.die(self)
    def polymorph(self,otype):
        """Note that this object becomes defunct and a new one is made.
        
        If there is a connected player, obviously the new one must be a 
        PlayableObject subtype."""
        if self.interface!=None:
            if not issubclass(otype,PlayableObject):
                raise TypeError("you cannot play as that!")
        new=otype(self.level,self.extra,play=0)
        #
        if self.interface!=None:
            new.play(self.interface)
        new.known=self.known
        if new.inventory!=None:
            new.inventory.die()
            new.inventory=self.inventory
        else:
            self.inventory.dump(self.pt)
            self.inventory.die()
        new.vitality=(self.vitality if self.vitality>new.maxhp else new.maxhp)
        #
        if self.status=="contained":
            self.container.insert(new)
            self.container.remove(self)
        elif self.status=="placed":
            new.place(*self.pt)
            self.lift()
        GridObject.all_objects.remove(self)
        if self is self.level.playerobj:
            self.level.playerobj=new
        if self.interface!=None:
            self.interface.playerobj=new
        self.level=None
        self.status="defunct"

