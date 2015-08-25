from repugeng.GeneratedLevel import GeneratedLevel
import random,math,sys

class MazeLevel2(GeneratedLevel):
    list_of_symbols={}
    coded_grid=""
    def _ligase_x(self,a,b):
        l=[]
        for i,j in zip(a,b):
            #XXX magic here
            if j[0]=="wall_TeeJnc_rt" and i[0]=="hwall":
                j=("wall_cross",None)
            if j[0]=="wall_corner_nw" and i[0]=="hwall":
                j=("wall_TeeJnc_dn",None)
            if i[0]=="hwall" and j[0]=="vwall":
                j=("wall_TeeJnc_lt",None)
            l.append((i,j))
        return map(list,zip(*l))
    def _ligase_y(self,a,b):
        if b[0][0]=="wall_TeeJnc_dn" and a[-1][0]=="vwall":
            b[0]=("wall_cross",None)
        if b[0][0]=="wall_corner_nw" and a[-1][0]=="vwall":
            b[0]=("wall_TeeJnc_rt",None)
        if a[-1][0]=="vwall" and b[0][0]=="hwall":
            b[0]=("wall_TeeJnc_up",None)
        return a+b
    def _join_grids_x(self,a,b):
        a[-1],b[0]=self._ligase_x(a[-1],b[0])
        return a+b
    def _join_grids_y(self,a,b):
        return [self._ligase_y(i[0][:],i[1][:]) for i in zip(a,b)]
    def _genroom(self,width,height):
        yield [("wall_corner_nw",None)]+(height-1)*[("vwall",None)]
        width-=1
        for i in range(width):
            yield [("hwall",None)]+(height-1)*[("floor1",None)]
    def _gendungeon(self,width,height):
        #Yes, 2 "not"s, i.e. "convert to bool" as no boolean xor so making do w/ bitwise
        if (not not random.randrange(3)) ^ (height<width):
            if width<4 or not random.randrange(2+int(abs(width-5)**self.sa)):
                return list(self._genroom(width,height))
            newwidth=random.randrange(2,width-1)
            return self._join_grids_x(self._gendungeon(newwidth,height),self._gendungeon(width-newwidth,height))
        else:
            if height<4 or not random.randrange(2+int(abs(height-5)**self.sa)):
                return list(self._genroom(width,height))
            newheight=random.randrange(2,height-1)
            return self._join_grids_y(self._gendungeon(width,newheight),self._gendungeon(width,height-newheight))
    def genmap(self,w=30,h=30,split_affinity=100):
        self.sa=split_affinity
        self.objgrid=self._gengrid(w,h)
        self.grid=self._gendungeon(w-1,h-1)
        self.grid=self._join_grids_x(self.grid,[[("wall_corner_ne",None)]+((h-2)*[("vwall",None)])])
        self.grid=self._join_grids_y(self.grid,[[("wall_corner_sw",None)]]+((w-2)*[[("hwall",None)]])+[[("wall_corner_se",None)]])
        self.gamut=[]
        for x,col in enumerate(self.grid):
            for y,cell in enumerate(col):
                if cell[0].startswith("floor"):
                    self.gamut.append((x,y))
        sp=random.choice(self.gamut)
        self.blazen=[]
        self.blazenext=[]
        self.walzen=[]
        self.nowalzen=[]
        self.bwalls=[]
        while len(self.blazen)<len(self.gamut):
            self.blazenext.append(sp)
            self.blaze()
            if not self.walzen:
                continue #This should only happen if it spat out a single huge room
            sp=random.choice(self.walzen)
            self.walzen.remove(sp)
            self.bwalls.append(sp)
            self.gamut.append(sp)
        for i in range(int(0.5+random.normalvariate(((w*h)**1.2)/1000,w))):
            #Add a few unneeded doors
            if self.nowalzen:
                x,y=sp=random.choice(self.nowalzen)
                #No widened doorways by sticking two adjacent doors
                if (x-1,y) not in self.bwalls \
                        and (x+1,y) not in self.bwalls \
                        and (x,y-1) not in self.bwalls \
                        and (x,y+1) not in self.bwalls:
                    self.nowalzen.remove(sp)
                    self.bwalls.append(sp)
                    self.gamut.append(sp)
        for x,y in self.bwalls:
            self.grid[x][y]=("floor1",None)
            self.gamut.remove((x,y))
    blazen=None
    blazenext=None
    walzen=None
    nowalzen=None
    bwalls=None
    def _bn(self,co):
        if co not in self.blazenext:
            self.blazenext.append(co)
    def blaze(self):
        while self.blazenext:
            x,y=self.blazenext.pop(0)
            if (x,y) not in self.blazen+self.walzen:
                #print (x,y),sorted(self.blazen)
                if (self.grid[x][y][0].startswith("floor")) or (x,y) in self.bwalls:
                    self.blazen.append((x,y))
                    if x>1:
                        self._bn((x-1,y))
                    if y>1:
                        self._bn((x,y-1))
                    if (x+2)<len(self.grid):
                        self._bn((x+1,y))
                    if (y+2)<len(self.grid[0]):
                        self._bn((x,y+1))
                else:
                    if self.grid[x][y][0] in ("vwall","hwall"):
                        if (x,y) not in self.nowalzen:
                            self.walzen.append((x,y))
            elif (x,y) in self.walzen:
                #Remove walls where the other side can be accessed already
                self.walzen.remove((x,y))
                self.nowalzen.append((x,y))
