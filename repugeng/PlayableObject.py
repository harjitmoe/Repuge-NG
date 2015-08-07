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
    myinterface=None
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
    def play(self,myinterface=None):
        """Connect to player."""
        if myinterface==None:
            myinterface=self.game.InterfaceClass(self,use_rpc=self.game.use_rpc)
        self.myinterface=myinterface
    def unplay(self):
        """Disconnect from player."""
        self.myinterface=None
    def conv_to_target(self,e):
        if e not in ("down","up","left","right","8","4","6","2","7","9","1","3","h","j","k","l","y","u","b","n"):
            return None
        if e in ("left", "4","h"): target=(self.pt[0]-1,self.pt[1])
        if e in ("down", "2","j"): target=(self.pt[0],self.pt[1]+1)
        if e in ("up",   "8","k"): target=(self.pt[0],self.pt[1]-1)
        if e in ("right","6","l"): target=(self.pt[0]+1,self.pt[1])
        if e in ("7","y"): target=(self.pt[0]-1,self.pt[1]-1)
        if e in ("9","u"): target=(self.pt[0]+1,self.pt[1]-1)
        if e in ("1","b"): target=(self.pt[0]-1,self.pt[1]+1)
        if e in ("3","n"): target=(self.pt[0]+1,self.pt[1]+1)
        return target
    def _PlayableObject__playercheck(self): #Two underscores
        if self.myinterface==None:
            return
        if self.level==None:
            return
        if self.vitality<=0:
            self.die()
            return
        self.level.redraw()
        if self.status!="placed":
            return
        if len(self.level.child_interfaces)>1:
            self.myinterface.push_message("Your turn.")
        e=self.myinterface.get_key_event()
        if e in ("\x03","\x04","\x1a"): #ETX ^C, EOT ^D, and ^Z
            #Does not go through to Python otherwise, meaning that Linux main terminals
            #are rendered otherwise out of order until someone kills Collecto
            #from a different terminal or over SSH (or rlogin).
            #This is relevant if someone is running this on an RPi.
            raise KeyboardInterrupt #^c, ^d or ^z pressed
        elif e in ("down","up","left","right","8","4","6","2","7","9","1","3","h","j","k","l","y","u","b","n"):
            target=self.conv_to_target(e)
            if self.game.debug_ghost or self.level.handle_move(target,self):
                self.place(*target)
        elif e=="#":
            name="#"+self.myinterface.ask_question("#")
            if name in ("#debug","#debugon"):
                self.game.debug=1
            elif self.game.debug:
                if name=="#debugoff":
                    self.game.debug=0
                elif name in ("#ghost","#ghoston"):
                    self.game.debug_ghost=1
                elif name=="#ghostoff":
                    self.game.debug_ghost=0
                elif name in ("#fovoff","#fovoffon","#clairvoyant","#allsight","#seeall"):
                    self.game.debug_fov_off=1
                elif name in ("#fov","#fovon","#fovoffoff","#clairvoyantoff","#allsightoff","#seealloff"):
                    self.game.debug_fov_off=0
                elif name.startswith("#passthrough "):
                    self.game.handle_command(name.split(" ",1)[1],self)
                elif name in ("#bugreport","#report","#gurumeditation","#guru"):
                    self.game._dump_report()
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
        if len(self.level.child_interfaces)>1:
            self.myinterface.push_message("Turn over.")
            self.myinterface.dump_messages()
    def up_hitpoint(self):
        if self.vitality<self.maxhp:
            self.vitality+=1
    def level_rebase(self,newlevel):
        GridObject.level_rebase(self,newlevel)
        if self.myinterface!=None:
            self.myinterface.level_rebase(newlevel)
    def die(self):
        if self.myinterface!=None:
            self.myinterface.ask_question("DYWYPI?")
            self.myinterface.close()
        GridObject.die(self)
    def polymorph(self,otype):
        """Note that this object becomes defunct and a new one is made.
        
        If there is a connected player, obviously the new one must be a 
        PlayableObject subtype."""
        if self.myinterface!=None:
            if not issubclass(otype,PlayableObject):
                raise TypeError("you cannot play as that!")
        novus=otype(self.game,self.extra,play=0)
        #
        if self.myinterface!=None:
            novus.play(self.myinterface)
        novus.known=self.known
        if novus.inventory!=None:
            novus.inventory.die()
            novus.inventory=self.inventory
        else:
            self.inventory.dump(self.pt)
            self.inventory.die()
        novus.vitality=(self.vitality if self.vitality>novus.maxhp else novus.maxhp)
        #
        if self.status=="contained":
            self.container.insert(novus)
            self.container.remove(self)
        elif self.status=="placed":
            novus.place(*self.pt+(self.level,))
            self.lift()
        GridObject.all_objects.remove(self)
        if self.myinterface!=None:
            self.myinterface.playerobj=novus
        self.level=None
        self.status="defunct"
        return novus
