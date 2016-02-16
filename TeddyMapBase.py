from ludicrous.Level import Level

import sys, random

class TeddyMapBase(Level):
    #More than one symbol per type can be defined: these
    # can then be distinguished in the run code
    list_of_symbols={"/":"wall_corner_nw","\\":"wall_corner_ne","`":"wall_corner_sw","'":"wall_corner_se","|":"vwall","-":"hwall",":":"vfeature","=":"hfeature"," ":"space",".":"floor1",",":"floor2","#":"floor3","T":"wall_TeeJnc_dn","^":"wall_TeeJnc_up",">":"wall_TeeJnc_rt","<":"wall_TeeJnc_lt","&":"staircase","%":"staircase"}
    #defined by subclass: coded_grid
    #defined by subclass: starting_pt
    #defined by subclass: title_window
    #defined by subclass: handle_staircase(self,playerobj)
    #optionally defined by subclass: bring_to_front(self, playerobj, whence="unspecified")

    def get_new_point(self):
        if not hasattr(self,"gamut"):
            self.gamut=[]
            for x in range(self.WIDTH):
                for y in range(self.HEIGHT):
                    if self.get_index_grid(x,y) and self.get_index_grid(x,y)[0].startswith("floor"):
                        self.gamut.append((x,y))
        while 1:
            (x,y)=random.choice(self.gamut)
            if (x,y) != self.starting_pt:
                return (x,y)

    def handle_move(self,target,playerobj):
        curstat=self.get_index_grid(*playerobj.pt)[0]
        nxtstat=self.get_index_grid(*target)[0]
        if curstat.startswith("floor"):
            floorlevel=type(0)(self.get_index_grid(*playerobj.pt)[0][5:])
        else:
            floorlevel=None
        if nxtstat.startswith("floor"):
            if floorlevel==None:
                return 1
            newlevel=type(0)(nxtstat[5:])
            if (newlevel-floorlevel)<=1:
                if (newlevel-floorlevel)==1:
                    playerobj.myinterface.push_message("You climb up")
                elif (newlevel-floorlevel)<0:
                    playerobj.myinterface.push_message("You jump down")
                return 1
            else:
                playerobj.myinterface.push_message("You try to climb but can't")
                return 0
        elif nxtstat in ("vfeature_open","hfeature_open"):
            return 1
        elif self.get_index_grid(*target)[1]=="%":
            playerobj.myinterface.push_message("Use Return (enter) to ascend.")
            return 1
        elif self.get_index_grid(*target)[1]=="&":
            playerobj.myinterface.push_message("Use Return (enter) to descend.")
            return 1
        elif self.get_index_grid(*target)[1]==":":
            kind,car=self.get_index_grid(*target)
            self.set_index_grid(("vfeature_open",car),*target)
            playerobj.myinterface.flush_fov()
            playerobj.myinterface.push_message("The door opens")
            return 0
        elif self.get_index_grid(*target)[1]=="=":
            kind,car=self.get_index_grid(*target)
            self.set_index_grid(("hfeature_open",car),*target)
            playerobj.myinterface.flush_fov()
            playerobj.myinterface.push_message("The door opens")
            return 0
        elif nxtstat=="space":
            playerobj.myinterface.push_message("You decide not to jump into the abyss")
            return 0
        else:
            playerobj.myinterface.push_message("You hit something")
            return 0
    
    def handle_command(self,e,playerobj):
        if e in (">","\r","\n","\r\n"," ","return","enter","space") and self.get_index_grid(*playerobj.pt)[0]=="staircase":
            self.handle_staircase(playerobj)
        elif e in ("o",):
            e2=playerobj.myinterface.get_key_event() #estraDiol (an oestrogen)
            target=playerobj.direction_to_target(playerobj.conv_to_direction(e2))
            if target!=None:
                kind,car=self.get_index_grid(*target)
                if kind.endswith("feature"):
                    kind+="_open"
                self.set_index_grid((kind,car),*target)
                playerobj.myinterface.flush_fov()
        elif e in ("c",):
            e2=playerobj.myinterface.get_key_event() #estraDiol (an oestrogen)
            target=playerobj.direction_to_target(playerobj.conv_to_direction(e2))
            if target!=None:
                kind,car=self.get_index_grid(*target)
                if kind.endswith("feature_open"):
                    kind=kind[:-5]
                self.set_index_grid((kind,car),*target)
                playerobj.myinterface.flush_fov()
        elif e=="i":
            return playerobj.report_inventory()
        elif e in ("t",):
            return playerobj.ask_throw()
        elif e in ("z",):
            return playerobj.ask_zap()
        elif e in (",","#pickup"):
            return playerobj.ask_pickup()
        elif e=="#quit":
            sys.exit()
