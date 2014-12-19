from utility import *
from Level import Level

class SampleMap(Level):
    coded_grid="""\
gooooooooooooG
d#,......,,,.jooooooo
d##......,,,#:...*...
d#,......,,,.gooooooo
jooooooooooooJ"""
    #More than one symbol per type can be defined: these
    # can then be distinguished in the run code
    list_of_symbols={"g":"wall_corner_nw","G":"wall_corner_ne","j":"wall_corner_sw","J":"wall_corner_se","d":"vwall","o":"hwall",":":"vfeature","*":"vfeature"," ":"space",".":"floor1",",":"floor2","#":"floor3"}

    def run(self):
        f=open("log.txt","w")
        self.objgrid[1][1]=("user",None)
        pt=(1,1)
        self.backend.goto_point(*pt)
        while 1:
            #print>>f,grid
            #print>>f,self.objgrid
            #print>>f
            self.redraw()
            e=self.backend.get_key_event()
            if e in ("down","up","left","right","8","4","6","2"):
                if e in ("down","2"): targit=(pt[0]+1,pt[1])
                if e in ("right","6"):targit=(pt[0],pt[1]+1)
                if e in ("up","8"):   targit=(pt[0]-1,pt[1])
                if e in ("left","4"): targit=(pt[0],pt[1]-1)
                floorlevel=type(0)(self.get_index_grid(*pt)[0][5:]) #XXX kludge/fragile/assumes
                curstat=self.get_index_grid(*pt)[0]
                nxtstat=self.get_index_grid(*targit)[0]
                if nxtstat.startswith("floor"):
                    newlevel=type(0)(nxtstat[5:])
                    if (newlevel-floorlevel)<=1:
                        if (newlevel-floorlevel)==1:
                            self.backend.push_message("You climb up")
                        elif (newlevel-floorlevel)<0:
                            self.backend.push_message("You jump down")
                        self.set_index_objgrid((),*pt)
                        pt=targit
                        self.set_index_objgrid(("user",None),*pt)
                        self.backend.goto_point(*pt[::-1])
                    else:
                        self.backend.push_message("You try to climb but can't")
                elif self.get_index_grid(*targit)[1]==":":
                    kind,car=self.get_index_grid(*targit)
                    self.set_index_grid(("floor2",car),*targit)
                    self.backend.push_message("The door opens")
                elif self.get_index_grid(*targit)[1]=="*":
                    kind,car=self.get_index_grid(*targit)
                    self.set_index_grid(("floor1",car),*targit)
                    self.backend.push_message("The door opens")
                elif nxtstat=="space":
                    self.backend.push_message("You decide not to jump into the abyss")
                else:
                    self.backend.push_message("You hit something")

if __name__=="__main__":
    SampleMap()

