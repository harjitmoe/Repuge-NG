from repugeng.PregenLevel import PregenLevel

class RoomLevel(PregenLevel):
    list_of_symbols={"g":"wall_corner_nw","G":"wall_corner_ne","j":"wall_corner_sw","J":"wall_corner_se","d":"vwall","o":"hwall",":":"vfeature","*":"vfeature"," ":"space",".":"floor1",",":"floor2","/":"floor3","$":"floor4","#":"floor5","P":"hfeature","l":"hfeature","v":"wall_TeeJnc_dn","^":"wall_TeeJnc_up",">":"wall_TeeJnc_rt","<":"wall_TeeJnc_lt","+":"wall_cross",}
    
    def genmap(self):
        self.coded_grid="g"+("o"*self.nsiz)+"G\n"+("d"+("."*self.nsiz)+"d\n")*self.nsiz+"j"+("o"*self.nsiz)+"J"
        self.readmap()
        gamutx=range(1,self.nsiz)
        gamuty=range(1,self.nsiz)
        self.gamut=[]
        for x in gamutx:
            for y in gamuty:
                self.gamut.append((x,y))
