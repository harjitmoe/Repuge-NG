import time
from repugeng.BackendSelector import BackendSelector
from repugeng.GridObject import GridObject
from repugeng.PlayerObject import PlayerObject
#n.b. put shadowtracer, when introduced, elsewhere (mixin?).

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
    #Debugging settings, nothing to see here
    debug=0
    bug_report={}
    debug_ghost=0
    debug_fov_off=0
    #
    def __init__(self,backend=None,debug_dummy=False):
        """Initialise the instance (this will run upon creation).
        
        By default: obtain a backend, initialise the grids, set the 
        player on self.starting_pt, draw the map, set window title to
        self.title_window and execute the run() method.
        
        A backend can be passed in as an argument, which is used for
        multi-level games (so as not to require a new window for each
        level).
        
        If starting_pt==None, skip that bit (level is expected to have
        an intro cutscene where the player character only appears 
        partway into it.
        
        Could be overridden by subclasses, but do remember to obtain a 
        self.backend by some means before trying to output anything.
        More recommended is to override run() and/or initmap().
        
        The debug_dummy argument allows a Level object to be created 
        without any of this initialisation step whatsoever, for 
        debugging purposes only.
        """
        if not debug_dummy:
            self.bug_report[__name__]={}
            try:
                if backend:
                    self.backend=backend
                else:
                    self.backend=BackendSelector.get_backend()
                self.initmap()
                self.redraw()
                if self.starting_pt!=None:
                    self.move_user(self.starting_pt)
                #Attempt to set title
                try:
                    self.backend.set_window_title(self.title_window)
                except NotImplementedError:
                    pass
                #Start the event loop
                self.run()
            except Exception,e:
                self.bug_report[__name__]["Exception"]=e
                self.bug_report[__name__]["grid"]=self.grid
                self.bug_report[__name__]["objgrid"]=self.objgrid
                self._dump_report()
                raise
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
        #*How I'd configured it dimension-wise when picking dimensions
        self.grid=self._gengrid(50,19)
        self.objgrid=self._gengrid(50,19)
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
    def redraw(self):
        """Draw the map (grid and objgrid).
        
        Presently this, by default, draws grid and (above it) objgrid at once
        and draws the entire grid.
        
        Unless you are a FOV engine, you probably don't want to override 
        this."""
        colno=0
        for col,col2 in zip(self.grid,self.objgrid):
            rowno=0
            for row,row2 in zip(col,col2):
                #print rowno,colno,col
                if row2:
                    self.backend.plot_tile(colno,rowno,row2[-1].tile)
                elif row:
                    self.backend.plot_tile(colno,rowno,row[0])
                rowno+=1
            colno+=1
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
            if self.playerobj not in self.objgrid[i[0]][i[1]]:
                self.objgrid[i[0]][i[1]].append(self.playerobj)
            self.backend.goto_point(*i)
            self.redraw()
            time.sleep(delay)
            self.objgrid[i[0]][i[1]].remove(self.playerobj)
        i=points[-1]
        self.objgrid[i[0]][i[1]].append(self.playerobj)
        self.backend.goto_point(*i)
        self.redraw()
        return i
    def followline(self,delay,points,obj):
        """Move a non-user object visibly down a list of points.
        (obj should be the object)."""
        import time
        for i in points[:-1]:
            self.objgrid[i[0]][i[1]].append(obj)
            self.redraw()
            time.sleep(delay)
            self.objgrid[i[0]][i[1]].remove(obj)
        self.objgrid[points[-1][0]][points[-1][1]].append(obj)
        self.redraw()
    def move_user(self,pt):
        """Move the user to pt.
        """
        if hasattr(self,"pt"): #i.e. not first run
            self.objgrid[self.pt[0]][self.pt[1]].remove(self.playerobj)
        else:
            self.playerobj=PlayerObject(self)
        self.objgrid[pt[0]][pt[1]].append(self.playerobj)
        self.backend.goto_point(*pt)
        self.pt=pt
        self.redraw()
    #
    def run(self):
        """Level entry point.  May be overridden by subclass.
        
        Default behaviour is an event loop.  Movement is passed to handle_move(...).
        Other commands are passed to handle_command(...).
        """
        self.initial_cutscene()
        while 1:
            self.redraw()
            e=self.backend.get_key_event()
            #self.backend.push_message(e)
            if e in ("\x03","\x04","\x1a"): #ETX ^C, EOT ^D, and ^Z
                #Does not go through to Python otherwise, meaning that Linux main terminals
                #are rendered otherwise out of order until someone kills Collecto
                #from a different terminal or over SSH (or rlogin).
                #This is relevant if someone is running this on an RPi.
                raise KeyboardInterrupt #^c, ^d or ^z pressed
            elif e in ("down","up","left","right","8","4","6","2"):
                if e in ("down","2"): target=(self.pt[0],self.pt[1]+1)
                if e in ("right","6"):target=(self.pt[0]+1,self.pt[1])
                if e in ("up","8"):   target=(self.pt[0],self.pt[1]-1)
                if e in ("left","4"): target=(self.pt[0]-1,self.pt[1])
                if self.debug_ghost or self.handle_move(target):
                    self.move_user(target)
            elif e=="#":
                name="#"+self.backend.ask_question("#")
                if name in ("#debug","#debugon"):
                    self.debug=1
                elif self.debug:
                    if name=="#debugoff":
                        self.debug=0
                    elif name in ("#ghost","#ghoston"):
                        self.debug_ghost=1
                    elif name=="#ghostoff":
                        self.debug_ghost=0
                    elif name in ("#fovoff","#fovoffon","#clairvoyant","#cranium","#allsight","#seeall"):
                        self.debug_fov_off=1
                    elif name in ("#fov","#fovon","#fovoffoff","clairvoyantoff","#craniumoff","#allsightoff","#seealloff"):
                        self.debug_fov_off=0
                    elif name.startswith("#passthrough "):
                        self.handle_command(name.split(" ",1)[1])
                    elif name in ("#bugreport","#report","#gurumeditation","#guru"):
                        self._dump_report()
                    else:
                        self.handle_command(name)
                else:
                    self.handle_command(name)
            else:
                self.handle_command(e)
            #Each creature gets a move:
            for file in self.objgrid:
                for stack in file:
                    for obj in stack:
                        obj.tick()
    #
    def _dump_report(self):
        import pickle,time
        f=open("bugreport.%010d.txt"%time.time(),"w")
        pickle.dump(self.bug_report,f)
        f.close()
    #
    def handle_move(self,dest):
        """Handle a move command by the user. --> True to go ahead or False 
        to block the move.
        
        Default allows no movement.  May be overridden by level subclass."""
        return 0
    #
    def handle_command(self,key_event):
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