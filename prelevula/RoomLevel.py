from ludicrous.GeneratedLevel import GeneratedLevel

class RoomLevel(GeneratedLevel):
    """A level generator creating a square room.
    
    Useful for testing level logic before trying it on a more complicated 
    level generator.
    """
    
    def genmap(self,nsiz=15):
        self.grid=self._gengrid(nsiz+2,nsiz+2)
        self.objgrid=self._gengrid(nsiz+2,nsiz+2)
        self.gamut=[]
        self.grid[0][0]=("wall_corner_nw",None)
        for x in range(1,nsiz+1):
            self.grid[x][0]=("hwall",None)
        self.grid[-1][0]=("wall_corner_ne",None)
        for y in range(1,nsiz+1):
            self.grid[0][y]=("vwall",None)
        self.grid[0][-1]=("wall_corner_sw",None)
        for x in range(1,nsiz+1):
            self.grid[x][-1]=("hwall",None)
        self.grid[-1][-1]=("wall_corner_se",None)
        for y in range(1,nsiz+1):
            self.grid[-1][y]=("vwall",None)
        for x in range(1,nsiz+1):
            for y in range(1,nsiz+1):
                self.grid[x][y]=("floor1",None)
                self.gamut.append((x,y))
