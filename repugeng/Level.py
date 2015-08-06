import time,sys,traceback
from repugeng.GridObject import GridObject
from repugeng.PlayableObject import PlayableObject
from repugeng.SimpleInterface import SimpleInterface

class Level(object):
    """Base class of a level.
    
    Notable attributes and methods (FIXME this is outdated):
    - run() - normally the level entrypoint.  Takes no args but self.
    - grid - list of lists of type-tuples for main level.
      A type-tuple is a tuple (type, extra_data) where extra_data is
      data internally used by the level code r.e. the status and 
      identity of the feature.  (Whereas type is just the tile type).
    - objgrid - list of lists of lists of stacked GridObject.
    - starting_pt - sets the initial location of the user.
    - pt - location of user at time of access.
    """
    WIDTH=100
    HEIGHT=100
    def __init__(self,game):
        self.game=game
        self.initmap()
        self.initialise()
    def bring_to_front(self, playerobj, whence="unspecified"):
        """To be called to make this level the active level for a 
        player, which may be anything from immediately after creation
        to never.
        
        The general idea is to take control of the player object, by 
        placing it on the level via its place(...) method.  The 
        mechanics of PlayableObject will then take care of hooking up
        that player's interface. 
        
        The whence argument specifies how the level was entered.
        Typically expected values are:
        
        - "starting"
        - "advancement"
        - "regression"
        - "jumping"
        - "unspecified"
        
        but a Game subclass may pass any object imaginable.  It is 
        paramount that those levels which process this are 
        compatible with the Game subclass with which they are used.
        """
        playerobj.place(self.starting_pt[0],self.starting_pt[1],self)
    def _gengrid(self,x,y):
        grid=[]
        for i in range(x):
            file=[] #row (x), file (y), stack (z)
            for j in range(y):
                file.append([])
            grid.append(file)
        return grid
    def readmap(self):
        """Generates self.grid from coded grid format.

        Whereas self.objgrid is generated empty.
        
        Coded grid format:
        
        - self.list_of_symbols is set to a character-to-tilename 
          mapping, maximum width 50 tiles, maximum height 19 tiles.
        - self.coded_grid is set to a multi-line string coding the map 
          using these symbols.
        
        The code characters used are included in the grid as extra data.
        So multiple internally different e.g. vfeature can be coded with 
        different characters and detected as different by the level code."""
        self.grid=self._gengrid(self.WIDTH,self.HEIGHT)
        self.objgrid=self._gengrid(self.WIDTH,self.HEIGHT)
        rowno=0
        for row in self.coded_grid.split("\n"):
            colno=0
            for col in row:
                self.grid[colno][rowno]=self.list_of_symbols[col],col
                colno+=1
            while len(row)<self.WIDTH:
                self.grid[len(row)][rowno]=("space"," ")
                row+=" "
            rowno+=1
        ##I forget the point of this.
        ##In any case, with the new standardisation measures on what is 
        ##x and what is y, it cuts a swathe through the display and model.
        ##So no.
        #for i in range(19-len(self.coded_grid.split("\n"))):
        #    self.grid[18-i]=[("space","")]*50
    def initmap(self):
        """Creates self.grid and self.objgrid.

        By default, calls readmap().
        
        This default behaviour may be overridden by subclasses.  General
        idea is that self.grid and self.objgrid are initialised."""
        self.readmap()
    #
    def initialise(self):
        """Ran after playerobj placed.  To be overridden by subclasses."""
        pass
    #
    def get_index_grid(self,x,y):
        return self.grid[x][y]
    def set_index_grid(self,v,x,y):
        self.grid[x][y]=v
    #
    # followline_user removed as obsolete and incompatible
    def followline(self,delay,points,obj):
        """Move a non-user object visibly down a list of points.
        (obj should be the object)."""
        import time
        for i in points[:-1]:
            self.objgrid[i[0]][i[1]].append(obj)
            time.sleep(delay)
            self.objgrid[i[0]][i[1]].remove(obj)
        self.objgrid[points[-1][0]][points[-1][1]].append(obj)
        obj.pt=points[-1]
    # move_user(self,pt) removed as obsolete, use PlayableObject.place
    #
    # run moved to Game, surprisingly
    #
    def handle_move(self,dest,playerobj):
        """Handle a move command by the user. --> True to go ahead or False 
        to block the move.
        
        Default allows no movement.  May be overridden by level subclass."""
        return 0
    #
    def handle_command(self,key_event,playerobj):
        r"""Handle a command by the user.  This is not called on move 
        commands by default.
        
        Default does nothing.  May be overridden by level subclass.
        
        BE AWARE THAT the same key may sent a different event on different 
        platforms/backends.  This much is not rigidly standardised between 
        backends.  Play safe: test key_event.lower() against ("return",
        "enter", "\r", "\n", "\r\n") for example."""
        return 0
    #
    # initial_cutscene removed as fundamentally incompatible with the 
    # new multi-user persistent-levels paradigm
    #
