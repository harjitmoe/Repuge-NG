"""From my proposal: The first thing I did was to produce a very simple level with no aim so I could see if what I was developing actually worked and correct errors as I made them. This consists of relatively sophisticated logic including doors and raised platforms, but no cutscenes."""

from repugeng.Level import Level

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
    starting_pt=(1,1)
    title_window="Basic Sample Repuge-NG Map"

    def handle_move(self,target):
        floorlevel=type(0)(self.get_index_grid(*self.pt)[0][5:]) #XXX kludge/fragile/assumes
        curstat=self.get_index_grid(*self.pt)[0]
        nxtstat=self.get_index_grid(*target)[0]
        if nxtstat.startswith("floor"):
            newlevel=type(0)(nxtstat[5:])
            if (newlevel-floorlevel)<=1:
                if (newlevel-floorlevel)==1:
                    self.backend.push_message("You climb up")
                elif (newlevel-floorlevel)<0:
                    self.backend.push_message("You jump down")
                return 1
            else:
                self.backend.push_message("You try to climb but can't")
                return 0
        elif self.get_index_grid(*target)[1]==":":
            kind,car=self.get_index_grid(*target)
            self.set_index_grid(("floor2",car),*target)
            self.backend.push_message("The door opens")
            return 0
        elif self.get_index_grid(*target)[1]=="*":
            kind,car=self.get_index_grid(*target)
            self.set_index_grid(("floor1",car),*target)
            self.backend.push_message("The door opens")
            return 0
        elif nxtstat=="space":
            self.backend.push_message("You decide not to jump into the abyss")
            return 0
        else:
            self.backend.push_message("You hit something")
            return 0

if __name__=="__main__":
    SampleMap()

