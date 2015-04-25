from repugeng.SimpleInterface import SimpleInterface
import math

class DumbFovInterface(SimpleInterface):
    """Dumb field of view.  An interface class which adds field of view support.
    
    Slow.
    """
    _fov_cache=None
    fov_status=1
    def _fov_check(self,x,y,passthrough_once=True):
        if (not self.fov_status) or (self.level.debug_fov_off):
            return True
        if not hasattr(self.level,"playerobj") or self.level.playerobj==None or self.level.playerobj.pt==None:
            return True
        if ((x,y) in self._fov_cache) and not passthrough_once:
            return self._fov_cache[(x,y)]
        if (x<0) or (y<0) or (x>=len(self.level.grid)) or (y>=len(self.level.grid[0])):
            return False
        
        vector_angle=math.atan2(abs(y-self.level.playerobj.pt[1]),abs(x-self.level.playerobj.pt[0]))
        vector_angle*=180
        vector_angle/=math.pi
        vector_angle=int(vector_angle+0.5)
        
        #Normal elif/else doesn't really work here
        ret=-1
        if ret==-1 and x==self.level.playerobj.pt[0] and y==self.level.playerobj.pt[1]:
            #Trace has reached the destination successfully
            ret=True
        if ret==-1 and self.level.grid[x][y] and (not self.level.grid[x][y][0].startswith("floor")) and not passthrough_once:
            #Blocking object has been encountered
            ret=False
        if ret==-1 and passthrough_once and self.level.grid[x][y] and (not self.level.grid[x][y][0].startswith("floor")):
            #From a wall: the actual path to the player obviously includes the floor, not more wall.
            if ret==-1 and vector_angle>0:
                n=self.level.grid[x][y-int(  (y-self.level.playerobj.pt[1])/abs(y-self.level.playerobj.pt[1])  )]
                if n and n[0].startswith("floor"):
                    ret=self._fov_check(x,y-int(  (y-self.level.playerobj.pt[1])/abs(y-self.level.playerobj.pt[1])  ),False)
            if ret==-1 and vector_angle<90:
                n=self.level.grid[x-int(  (x-self.level.playerobj.pt[0])/abs(x-self.level.playerobj.pt[0])  )][y]
                if n and n[0].startswith("floor"):
                    ret=self._fov_check(x-int(  (x-self.level.playerobj.pt[0])/abs(x-self.level.playerobj.pt[0])  ),y,False)
            if ret==-1 and vector_angle>0 and vector_angle<90:
                n=self.level.grid[x-int(  (x-self.level.playerobj.pt[0])/abs(x-self.level.playerobj.pt[0])  )][y-int(  (y-self.level.playerobj.pt[1])/abs(y-self.level.playerobj.pt[1])  )]
                if n and n[0].startswith("floor"):
                    ret=self._fov_check(x-int(  (x-self.level.playerobj.pt[0])/abs(x-self.level.playerobj.pt[0])  ),y-int(  (y-self.level.playerobj.pt[1])/abs(y-self.level.playerobj.pt[1])  ),False)
        if ret==-1 and vector_angle>=75:
            #Vertical is closest approximation for now
            ret=self._fov_check(x,y-int(  (y-self.level.playerobj.pt[1])/abs(y-self.level.playerobj.pt[1])  ),False)
        if ret==-1 and vector_angle>=15:
            #45deg is closest approximation for now
            ret=self._fov_check(x-int(  (x-self.level.playerobj.pt[0])/abs(x-self.level.playerobj.pt[0])  ),y-int(  (y-self.level.playerobj.pt[1])/abs(y-self.level.playerobj.pt[1])  ),False)
        if ret==-1:
            #Horizontal is closest approximation for now
            ret=self._fov_check(x-int(  (x-self.level.playerobj.pt[0])/abs(x-self.level.playerobj.pt[0])  ),y,False)

        if not passthrough_once:
            self._fov_cache[(x,y)]=ret
        return ret
    def redraw(self):
        """Draw the map (grid and objgrid)."""
        if self.level.playerobj.pt:
            self.backend.goto_point(*self.get_viewport_pt())
        colno=0
        self._fov_cache={}
        for coordscol,col,col2 in zip(*self.get_viewport_grids()):
            rowno=0
            for coords,row,row2 in zip(coordscol,col,col2):
                #print colno,rowno,col
                if self._fov_check(*coords):
                    if row2:
                        self.backend.plot_tile(colno,rowno,row2[-1].tile)
                    elif row:
                        self.backend.plot_tile(colno,rowno,row[0])
                else:
                    self.backend.plot_tile(colno,rowno,"space")
                rowno+=1
            colno+=1
