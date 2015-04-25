from repugeng.GridObject import GridObject
class PlayerObject(GridObject):
    """A grid object with an attached interface, controlled by the player.
    """
    tile="user"
    def tick(self):
        self.interface.redraw()
        e=self.interface.backend.get_key_event()
        if e in ("\x03","\x04","\x1a"): #ETX ^C, EOT ^D, and ^Z
            #Does not go through to Python otherwise, meaning that Linux main terminals
            #are rendered otherwise out of order until someone kills Collecto
            #from a different terminal or over SSH (or rlogin).
            #This is relevant if someone is running this on an RPi.
            raise KeyboardInterrupt #^c, ^d or ^z pressed
        elif e in ("down","up","left","right","8","4","6","2"):
            if e in ("down","2"): target=(self.pt[0],self.pt[1]+1)
            if e in ("right","6"):target=(self.pt[0]+1,self.pt[1])
            if e in ("up","8"):   target=(self.pt[0],self.pt[1]-1)
            if e in ("left","4"): target=(self.pt[0]-1,self.pt[1])
            if self.level.debug_ghost or self.level.handle_move(target):
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
                    self.level.handle_command(name.split(" ",1)[1])
                elif name in ("#bugreport","#report","#gurumeditation","#guru"):
                    self.level._dump_report()
                elif name in ("#testerror"):
                    raise RuntimeError("testing error handler")
                elif name in ("#abort","#abrt","#kill"):
                    import os
                    os.abort()
                else:
                    self.level.handle_command(name)
            else:
                self.level.handle_command(name)
        else:
            self.level.handle_command(e)
    def level_rebase(self,newlevel):
        self.level=newlevel
        self.interface.level=newlevel
