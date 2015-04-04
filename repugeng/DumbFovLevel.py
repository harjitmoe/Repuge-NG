from repugeng.Level import Level
import math

class DumbFovLevel(Level):
    """Dumb field of view.  A subclass for Level which adds field of view support.
    
    Slow.
    """
    _fov_cache=None
    fov_status=1
    def _fov_check(self,x,y,passthrough_once=True):
        if not self.fov_status:
            return True
        if not hasattr(self,"pt"):
            return True
        if ((x,y) in self._fov_cache) and not passthrough_once:
            return self._fov_cache[(x,y)]
        
        vector_angle=math.atan2(abs(y-self.pt[1]),abs(x-self.pt[0]))
        vector_angle*=180
        vector_angle/=math.pi
        vector_angle=int(vector_angle+0.5)
        
        #Normal elif/else doesn't really work here
        ret=-1
        if ret==-1 and x==self.pt[0] and y==self.pt[1]:
            #Trace has reached the destination successfully
            ret=True
        if ret==-1 and self.grid[x][y] and (not self.grid[x][y][0].startswith("floor")) and not passthrough_once:
            #Blocking object has been encountered
            ret=False
        if ret==-1 and passthrough_once and self.grid[x][y] and (not self.grid[x][y][0].startswith("floor")):
            #From a wall: the actual path to the player obviously includes the floor, not more wall.
            if ret==-1 and vector_angle>0:
                n=self.grid[x][y-int(  (y-self.pt[1])/abs(y-self.pt[1])  )]
                if n and n[0].startswith("floor"):
                    ret=self._fov_check(x,y-int(  (y-self.pt[1])/abs(y-self.pt[1])  ),False)
            if ret==-1 and vector_angle<90:
                n=self.grid[x-int(  (x-self.pt[0])/abs(x-self.pt[0])  )][y]
                if n and n[0].startswith("floor"):
                    ret=self._fov_check(x-int(  (x-self.pt[0])/abs(x-self.pt[0])  ),y,False)
            if ret==-1 and vector_angle>0 and vector_angle<90:
                n=self.grid[x-int(  (x-self.pt[0])/abs(x-self.pt[0])  )][y-int(  (y-self.pt[1])/abs(y-self.pt[1])  )]
                if n and n[0].startswith("floor"):
                    ret=self._fov_check(x-int(  (x-self.pt[0])/abs(x-self.pt[0])  ),y-int(  (y-self.pt[1])/abs(y-self.pt[1])  ),False)
        if ret==-1 and vector_angle>=75:
            #Vertical is closest approximation for now
            ret=self._fov_check(x,y-int(  (y-self.pt[1])/abs(y-self.pt[1])  ),False)
        if ret==-1 and vector_angle>=15:
            #45deg is closest approximation for now
            ret=self._fov_check(x-int(  (x-self.pt[0])/abs(x-self.pt[0])  ),y-int(  (y-self.pt[1])/abs(y-self.pt[1])  ),False)
        if ret==-1:
            #Horizontal is closest approximation for now
            ret=self._fov_check(x-int(  (x-self.pt[0])/abs(x-self.pt[0])  ),y,False)

        if not passthrough_once:
            self._fov_cache[(x,y)]=ret
        return ret
    def redraw(self):
        """Draw the map (grid and objgrid)."""
        colno=0
        self._fov_cache={}
        for col,col2 in zip(self.grid,self.objgrid):
            rowno=0
            for row,row2 in zip(col,col2):
                #print colno,rowno,col
                if self._fov_check(colno,rowno):
                    if row2:
                        self.backend.plot_tile(colno,rowno,row2[0])
                    elif row:
                        self.backend.plot_tile(colno,rowno,row[0])
                else:
                    self.backend.plot_tile(colno,rowno,"space")
                rowno+=1
            colno+=1
