import time,sys,traceback
from repugeng.GridObject import GridObject
from repugeng.PlayableObject import PlayableObject
from repugeng.SimpleInterface import SimpleInterface

class Level(object):
    """Base class of a level.
    
    Notable attributes and methods:
    - run() - normally the level entrypoint.  Takes no args but self.
    - grid - list of lists of type-tuples for main level.
      A type-tuple is a tuple (type, extra_data) where extra_data is
      data internally used by the level code r.e. the status and 
      identity of the feature.  (Whereas type is just the tile type).
    - objgrid - list of lists of lists of stacked GridObject.
    - starting_pt - sets the initial location of the user.
    - pt - location of user at time of access.
    """
    def __init__(self,game,start):
        self.game=game
        self.initmap()
        self.game.playerobj.place(self.starting_pt[0],self.starting_pt[1],self)
        self.initialise()
        #Start the event loop
        if start:
            self.run()
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
        #Width 50 not 80 as 16x16 tiles are a conceivable backend and
        #my monitor's max res is 1024x768
        #Height 19 as this is the maximum height to avoid lxterminal 
        #scrolling (thus shifting the viewport aaaargggggghhhh)*
        #*How I'd configured it dimension-wise when picking dimensions, thatis
        self.grid=self._gengrid(100,100)
        self.objgrid=self._gengrid(100,100)
        rowno=0
        for row in self.coded_grid.split("\n"):
            colno=0
            for col in row:
                self.grid[colno][rowno]=self.list_of_symbols[col],col
                colno+=1
            while len(row)<50:
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
    def followline_user(self,delay,points):
        """Move the user visibly down a list of points."""
        import time
        for i in points[:-1]:
            if self.game.playerobj not in self.objgrid[i[0]][i[1]]:
                self.objgrid[i[0]][i[1]].append(self.game.playerobj)
            time.sleep(delay)
            self.objgrid[i[0]][i[1]].remove(self.game.playerobj)
        i=points[-1]
        self.objgrid[i[0]][i[1]].append(self.game.playerobj)
        return i
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
    def run(self,resume=0):
        """Level entry point.  May be overridden by subclass.
        
        Default behaviour is an event loop.  Movement is passed to handle_move(...).
        Other commands are passed to handle_command(...).
        
        Resume is nonzero when being resumed from a save (TODO implement saving).
        """
        if not resume:
            self.initial_cutscene()
        while 1:
            #Each creature gets a move:
            for obj in GridObject.all_objects:
                obj.tick()
    #
    def _dump_report(self):
        import pickle,time
        f=open("bugreport.%010d.txt"%time.time(),"w")
        pickle.dump(self.bug_report,f)
        f.close()
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
    def initial_cutscene(self):
        """Hook called by default implementation of run() before the event loop"""
        pass
    #
