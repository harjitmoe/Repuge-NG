from repugeng.GeneratedLevel import GeneratedLevel

class MazeLevel(GeneratedLevel):
    """A level generator for a square maze.

    This maze is generated using a *modified* DFS sweep, modified 
    in that leaf nodes can sometimes end up connected to 
    geographically adjacent nodes, thus rendering the maze not 
    necessarily acyclic.
    """
    list_of_symbols={"g":"wall_corner_nw","G":"wall_corner_ne","j":"wall_corner_sw","J":"wall_corner_se","d":"vwall","o":"hwall",":":"vfeature","*":"vfeature"," ":"space",".":"floor1",",":"floor2","/":"floor3","$":"floor4","#":"floor5","P":"hfeature","l":"hfeature","v":"wall_TeeJnc_dn","^":"wall_TeeJnc_up",">":"wall_TeeJnc_rt","<":"wall_TeeJnc_lt","+":"wall_cross",}
    def genmaze(self,nsiz):
        """Return a list of wall co-ordinates to break in grid output to produce a maze.
        
        This is a *modified* DFS sweep, modified in that leaf nodes 
        can sometimes end up connected to geographically adjacent 
        nodes, thus rendering the maze not necessarily acyclic.  I 
        have decided that this is a feature, not a bug, and have 
        decided not to fix that which is not broken."""
        import random
        cells_traversed=[(0,0)]
        broken_walls=[] #The *output* of the traversal
        depth=[(0,0)]
        while depth!=[]:
            x,y=depth[-1]
            #print x,y
            try:
                next=[[x-1,y],[x,y-1],[x+1,y],[x,y+1]]
                next=filter((lambda u,c=cells_traversed:(u not in c)),next)
                next=filter((lambda u,c=cells_traversed:(u[0]>=0) and (u[1]>=0)),next)
                next=filter((lambda u,c=cells_traversed,n=nsiz:(u[0]<n) and (u[1]<n)),next)
                next=random.choice(tuple(next))
            except IndexError: #EAFP
                depth.pop() #Pop rightmost value
                continue
            depth.append(next)
            cells_traversed.append(next)
            nox,noy=depth[-1]
            if nox!=x:
                broken_walls.append((nox+x+1,y*2+1))
            if noy!=y:
                broken_walls.append((x*2+1,noy+y+1))
        return broken_walls
    
    def genmap(self,nsiz=12): #Limited by sanity - too large is effectively unexitable
        #Generate a grid of walled cells, as a maze predecessor.
        self.coded_grid="g"+("ov"*(nsiz-1))+"oG\n"
        self.coded_grid+=("d"+(".d"*(nsiz)+"\n")+(">"+("o+"*(nsiz-1))+"o<\n"))*(nsiz-1)
        self.coded_grid+=("d"+(".d"*(nsiz-1))+".d\n")
        self.coded_grid+="j"+("o^"*(nsiz-1))+"oJ"
        self.readmap()
        #Remove walls to form maze, changing type of surrounding junction cells as required
        bwalls=self.genmaze(nsiz)
        for y,x in bwalls: 
            self.grid[x][y]=("floor1",".")
            if self.grid[x-1][y][0]=="wall_cross":
                self.grid[x-1][y]=("wall_TeeJnc_lt","+")
            elif self.grid[x-1][y][0]=="wall_TeeJnc_rt":
                self.grid[x-1][y]=("vwall","+")
            elif self.grid[x-1][y][0]=="wall_TeeJnc_up":
                self.grid[x-1][y]=("wall_corner_se","+")
            elif self.grid[x-1][y][0]=="wall_TeeJnc_dn":
                self.grid[x-1][y]=("wall_corner_ne","+")
            elif self.grid[x-1][y]==("wall_corner_sw","+"): #DO this time need to check subclass symbol
                self.grid[x-1][y]=("vwall","+")
            elif self.grid[x-1][y]==("wall_corner_nw","+"): #DO this time need to check subclass symbol
                self.grid[x-1][y]=("vwall","+")
            if self.grid[x+1][y][0]=="wall_cross":
                self.grid[x+1][y]=("wall_TeeJnc_rt","+")
            elif self.grid[x+1][y][0]=="wall_TeeJnc_lt":
                self.grid[x+1][y]=("vwall","+")
            elif self.grid[x+1][y][0]=="wall_TeeJnc_up":
                self.grid[x+1][y]=("wall_corner_sw","+")
            elif self.grid[x+1][y][0]=="wall_TeeJnc_dn":
                self.grid[x+1][y]=("wall_corner_nw","+")
            elif self.grid[x+1][y]==("wall_corner_se","+"): #DO this time need to check subclass symbol
                self.grid[x+1][y]=("vwall","+")
            elif self.grid[x+1][y]==("wall_corner_ne","+"): #DO this time need to check subclass symbol
                self.grid[x+1][y]=("vwall","+")
            #
            if self.grid[x][y-1][0]=="wall_cross":
                self.grid[x][y-1]=("wall_TeeJnc_up","+")
            elif self.grid[x][y-1][0]=="wall_TeeJnc_dn":
                self.grid[x][y-1]=("hwall","+")
            elif self.grid[x][y-1][0]=="wall_TeeJnc_lt":
                self.grid[x][y-1]=("wall_corner_se","+")
            elif self.grid[x][y-1][0]=="wall_TeeJnc_rt":
                self.grid[x][y-1]=("wall_corner_sw","+")
            elif self.grid[x][y-1]==("wall_corner_ne","+"): #DO this time need to check subclass symbol
                self.grid[x][y-1]=("hwall","+")
            elif self.grid[x][y-1]==("wall_corner_nw","+"): #DO this time need to check subclass symbol
                self.grid[x][y-1]=("hwall","+")
            if self.grid[x][y+1][0]=="wall_cross":
                self.grid[x][y+1]=("wall_TeeJnc_dn","+")
            elif self.grid[x][y+1][0]=="wall_TeeJnc_up":
                self.grid[x][y+1]=("hwall","+")
            elif self.grid[x][y+1][0]=="wall_TeeJnc_lt":
                self.grid[x][y+1]=("wall_corner_ne","+")
            elif self.grid[x][y+1][0]=="wall_TeeJnc_rt":
                self.grid[x][y+1]=("wall_corner_nw","+")
            elif self.grid[x][y+1]==("wall_corner_se","+"): #DO this time need to check subclass symbol
                self.grid[x][y+1]=("hwall","+")
            elif self.grid[x][y+1]==("wall_corner_sw","+"): #DO this time need to check subclass symbol
                self.grid[x][y+1]=("hwall","+")
        self.gamut=[]
        xs=[(i*2)+1 for i in range(1,nsiz)]
        for x in xs:
            y=[(i*2)+1 for i in range(1,nsiz)]
            self.gamut.extend(zip([x]*nsiz,y))
