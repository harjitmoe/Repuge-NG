from repugeng.GridObject import GridObject
from repugeng.Container import Container

class PlayerObject(GridObject):
    """A grid object with an attached interface, controlled by the player.
    """
    tile="user"
    vitality=10
    known=None
    maxhp=10
    name="player"
    appearance="player"
    def initialise(self,noinit):
        """Just been spawned.  Do what?"""
        if not noinit:
            self.interface=self.level.InterfaceClass(self)
            self.known=[]
            self.inventory=Container(self.level)
        self.add_handler(1,self.onetick)
        self.add_handler(5,self.up_hitpoint)
    def onetick(self):
        if self.vitality<=0:
            self.die()
            return
        self.interface.redraw()
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
                self.level.move_user(target)
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
        self.level=newlevel
        self.interface.level=newlevel
        self.inventory.level_rebase(newlevel)
    def die(self):
        self.lift()
        GridObject.all_objects.remove(self)
        self.level=None
        self.status="defunct"
        self.interface.backend.ask_question("DYWYPI?")
        self.interface.close()
    def polymorph(self,otype):
        """Note that this object becomes defunct and a new one is made.
        
        Obviously the new one must support interaction."""
        new=otype(self.level,self.extra,noinit=1)
        #
        new.interface=self.interface
        new.known=self.known
        new.inventory=self.inventory
        #
        new.inventory.die()
        new.inventory=self.inventory
        if self.status=="contained":
            self.container.remove(self)
        elif self.status=="placed":
            new.place(*self.pt)
            self.lift()
        GridObject.all_objects.remove(self)
        self.level=None
        self.status="defunct"

