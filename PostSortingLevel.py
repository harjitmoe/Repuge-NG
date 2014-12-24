#The first one I made (bar samplemap) and the most klu[d]ged yet.  Based on PC
import sys, time
from repugeng.Level import Level
from repugeng.MultilevelStorage import MultilevelStorage

class PostSortingLevel(Level):
    coded_grid="""\
              goooooooooooooooooG
              d####$$$$////,,,..jooG
              d####$$$$////,,,.....d
              d##goooooooooooG.....d
              d##d           d..gooJ
gooPPPoooooooG8PP9           d..*
d............jJ##d           d..jooo
d.........,/$####d           d..,/$#
*.........,/$####d           *..,/$#
d.........,/$####d           d..,/$#
d............gG##d           d..gooo
joo...oooooooJd##d           d..*
              d##d           d..jooG
              d##joooooooooooJ.....d
              d####$$$$////,,,.....d
              d####$$$$////,,,..gooJ
              joooooooooooooooooJ"""
    #More than one symbol per type can be defined: these
    # can then be distinguished in the run code
    list_of_symbols={"g":"wall_corner_nw","G":"wall_corner_ne","j":"wall_corner_sw","J":"wall_corner_se","d":"vwall","o":"hwall",":":"vfeature","*":"vfeature"," ":"space",".":"floor1",",":"floor2","/":"floor3","$":"floor4","#":"floor5","P":"hfeature","8":"wall_TeeJnc_rt","9":"wall_TeeJnc_lt"}
    starting_pt=None
    title_window="Harry Potter"
    def initial_cutscene(self):
        self.hpbeancount=MultilevelStorage("hpbeancount")
        self.hpbeancount.initialise_property("beans",0)
        points=[(4,6+5),(4,5+5),(5,4+5),(6,3+5),(7,3+5),(8,3+5),(9,3+5),(10,3+5),(11,3+5),(12,3+5),(13,3+5),(14,8),(15,8),(15,9),(15,10),(15,11),(15,12),(15,13),(15,14),(16,14),(17,14),(18,14),(19,14),(20,14),(21,14),(22,14),(23,14),(24,14),(25,14),(26,14),(27,14),(28,14),(29,14),(30,14),(30,13),(30,12),(30,11),(30,10),(30,9),(31,9),(32,9),(33,9),(34,9),(35,9)]
        loza=[] #More snappy than "extras streaming from GH" ;-)
        while len(loza)<len(points):
            #Be lazy: create the appearance of people streaming out of
            # GH but actually extend stream at its end
            loza.append(points[len(loza)])
            #XXX reverse lozapts inplace!!!
            self.set_index_objgrid(("extra",None),*loza[-1])
            self.redraw()
            time.sleep(0.1)
        #Still lazy: remove the first loza not the last/flowthrough
        self.set_index_objgrid(("user",None),*loza[0]) #Harry!
        self.set_index_objgrid(("ron",None),16,12) #Ron!
        self.set_index_objgrid(("dumbledore",None),13,7) #Dumbledore!
        ddchain=[(13,7),(13,8),(12,8),(11,8),(10,8),(9,8),(8,8),(7,8),(6,8)]
        pt=loza[0]
        self.backend.goto_point(*pt)
        loza.pop(0)
        self.redraw()
        time.sleep(0.1)
        while loza:
            #Illusion of students going upstairs leaving HP
            self.set_index_objgrid((),*loza[0])
            loza.pop(0)
            self.redraw()
            time.sleep(0.1)
        #HP comes in
        for i in points[0:3]:
            self.set_index_objgrid(("user",None),*i)
            self.move_user(i)
            self.redraw()
            time.sleep(0.1)
            if i!=points[2]:
                self.set_index_objgrid((),*i)
        #AD comes down
        for i in ddchain:
            self.set_index_objgrid(("dumbledore",None),*i)
            self.redraw()
            time.sleep(0.1)
            if i!=ddchain[-1]:
                self.set_index_objgrid((),*i)
        #Instruction
        self.set_index_grid(("hfeature","great hall door"),3,6+5)
        self.set_index_grid(("hfeature","great hall door"),4,6+5)
        self.set_index_grid(("hfeature","great hall door"),5,6+5)
        self.redraw()
        self.set_index_objgrid(("fred",None),32,14)
        self.redraw()
        self.set_index_objgrid(("bean",None),31,14)
        self.redraw()
        self.set_index_objgrid(("fred",None),32,13) #Actually George
        self.redraw()
        self.backend.slow_push_message("I am Albus Dumbledore, your headmaster.  Now Hogwarts is full of secrets, Harry, so search behind every door; but keep in mind, not all secrets are rewarding!  Your first lesson is on the Third Floor, Mr Potter.  Off you go!","AD: ")
        self.backend.dump_messages()
#
if __name__=="__main__":
    PostSortingLevel()
