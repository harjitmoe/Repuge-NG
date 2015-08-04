from repugeng.Level import Level
from CollectoInterface import CollectoInterface

class TeddyMapU(Level):
    #Raw string (r""") because backslashes
    # Grace  Bathroom
    # Tedd   Edward
    # (or a 360deg rotation thereof)
    coded_grid=r"""



/------------T-----T------------\
|............|.....|............|
|............:.....:............|
|............|.....|............|
|............|.|...|............|
>------------<.|...>------------<
|............|&|...|............|
|............>-'...|............|
|............:.....:............|
|............|.....|............|
`------------^-----^------------'
"""
    #More than one symbol per type can be defined: these
    # can then be distinguished in the run code
    list_of_symbols={"/":"wall_corner_nw","\\":"wall_corner_ne","`":"wall_corner_sw","'":"wall_corner_se","|":"vwall","-":"hwall",":":"vfeature","=":"hfeature"," ":"space",".":"floor1",",":"floor2","#":"floor3","T":"wall_TeeJnc_dn","^":"wall_TeeJnc_up",">":"wall_TeeJnc_rt","<":"wall_TeeJnc_lt","&":"staircase","%":"staircase"}
    starting_pt=(14,10)
    title_window="Basic Sample Repuge-NG Map"

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
                    playerobj.myinterface.backend.push_message("You climb up")
                elif (newlevel-floorlevel)<0:
                    playerobj.myinterface.backend.push_message("You jump down")
                return 1
            else:
                playerobj.myinterface.backend.push_message("You try to climb but can't")
                return 0
        elif nxtstat in ("vfeature_open","hfeature_open"):
            return 1
        elif self.get_index_grid(*target)[1]=="%":
            playerobj.myinterface.backend.push_message("Use Return (enter) to ascend.")
            return 1
        elif self.get_index_grid(*target)[1]=="&":
            playerobj.myinterface.backend.push_message("Use Return (enter) to descend.")
            return 1
        elif self.get_index_grid(*target)[1]==":":
            kind,car=self.get_index_grid(*target)
            self.set_index_grid(("vfeature_open",car),*target)
            playerobj.myinterface.flush_fov()
            playerobj.myinterface.backend.push_message("The door opens")
            return 0
        elif self.get_index_grid(*target)[1]=="=":
            kind,car=self.get_index_grid(*target)
            self.set_index_grid(("hfeature_open",car),*target)
            playerobj.myinterface.flush_fov()
            playerobj.myinterface.backend.push_message("The door opens")
            return 0
        elif nxtstat=="space":
            playerobj.myinterface.backend.push_message("You decide not to jump into the abyss")
            return 0
        else:
            playerobj.myinterface.backend.push_message("You hit something")
            return 0
    
    def handle_command(self,e,playerobj):
        if e in (">","\r","\n","\r\n"," ","return","enter","space") and self.get_index_grid(*playerobj.pt)[0]=="staircase":
            raise self.game.RegressLevelException
        elif e in ("o",):
            e2=playerobj.myinterface.backend.get_key_event() #estraDiol (an oestrogen)
            target=playerobj.conv_to_target(e2)
            if target!=None:
                kind,car=self.get_index_grid(*target)
                if kind.endswith("feature"):
                    kind+="_open"
                self.set_index_grid((kind,car),*target)
                playerobj.myinterface.flush_fov()
        elif e in ("c",):
            e2=playerobj.myinterface.backend.get_key_event() #estraDiol (an oestrogen)
            target=playerobj.conv_to_target(e2)
            if target!=None:
                kind,car=self.get_index_grid(*target)
                if kind.endswith("feature_open"):
                    kind=kind[:-5]
                self.set_index_grid((kind,car),*target)
                playerobj.myinterface.flush_fov()
        elif e=="#quit":
            sys.exit()
