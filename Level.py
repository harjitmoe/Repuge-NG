import time
from BackendSelector import BackendSelector
#n.b. put shadowtracer, when introduced, elsewhere.

class Level(object):
    def __init__(self):
        self.backend=BackendSelector.get_backend()
        self.readmap()
        self.redraw()
        self.run()
    def _gengrid(self,x,y):
        grid=[]
        for i in range(y):
            row=[]
            for j in range(x):
                row.append([])
            grid.append(row)
        return grid
    def readmap(self):
        #Width 50 not 80 as 16x16 tiles are a conceivable backend and
        #my monitor's max res is 1024x768
        #Height 19 as this is the maximum height to avoid lxterminal 
        #scrolling (thus shifting the viewport aaaargggggghhhh)
        self.grid=self._gengrid(50,19)
        self.objgrid=self._gengrid(50,19)
        rowno=0
        for row in self.coded_grid.split("\n"):
            colno=0
            for col in row:
                self.grid[rowno][colno]=self.list_of_symbols[col],col
                colno+=1
            while len(row)<50:
                self.grid[rowno][len(row)]=("space"," ")
                row+=" "
            rowno+=1
        for i in range(19-len(self.coded_grid.split("\n"))):
            self.grid[18-i]=[("space","")]*50
        #return self.grid,self.objgrid,self.run
    def drawmap(self,grid,ogrid):
        #A much older version, from before the introduction of shadowtracing, for now.
        rowno=0
        for row,row2 in zip(self.grid,self.objgrid):
            colno=0
            for col,col2 in zip(row,row2):
                #print rowno,colno,col
                if col2:
                    self.backend.plot_tile(rowno,colno,col2[0])
                elif col:
                    self.backend.plot_tile(rowno,colno,col[0])
                colno+=1
            rowno+=1
    #
    def get_index_grid(self,a,b):
        return self.grid[a][b]
    def get_index_objgrid(self,a,b):
        return self.objgrid[a][b]
    def set_index_grid(self,v,a,b):
        self.grid[a][b]=v
    def set_index_objgrid(self,v,a,b):
        self.objgrid[a][b]=v
    #
    def followline_user(self,delay,points):
        import time
        for i in points[:-1]:
            self.set_index_objgrid(("user",None),*i[::-1])
            pt=i[::-1]
            self.backend.goto_point(*pt[::-1])
            self.redraw()
            time.sleep(delay)
            self.set_index_objgrid((),*i[::-1])
        i=points[-1]
        self.set_index_objgrid(("user",None),*i[::-1])
        pt=i[::-1]
        self.backend.goto_point(*pt[::-1])
        self.redraw()
        return pt
    def followline(self,delay,points,typeo):
        import time
        for i in points[:-1]:
            self.set_index_objgrid(typeo,*i[::-1])
            self.redraw()
            time.sleep(delay)
            self.set_index_objgrid((),*i[::-1])
        self.set_index_objgrid(typeo,*points[-1][::-1])
        self.redraw()
    def redraw(self):
        self.drawmap(self.grid,self.objgrid)
    def move_user(self,pt1,pt2):
        self.set_index_objgrid((),*pt1)
        self.set_index_objgrid(("user",None),*pt2)
        self.backend.goto_point(*pt2[::-1])
        self.redraw()
    #
    def run(self):
        raise NotImplementedError,"should be implemented by level subclass"
    #