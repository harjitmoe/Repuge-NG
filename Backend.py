import textwrap

class Backend(object):
    """The backend interface.  This is the core of Repuge-NG, although ideally
    the level need not know about it (not so much in practice).
    
    Do not create an instance directly.
    
    Obtain an instance using BackendSelector.get_backend().  The class 
    itself is a portable interface which does not implement anything 
    interface-dependant (accordingly it implements only the storage for the 
    -- More -- system).  Actual functionality is obtained from platform- and
    interface-specific subclasses, a working one of which should be usable
    by calling BackendSelector.get_backend() to get an instance.
    
    There is not necessarily multiple-window support, so creating multiple
    Backend is not guaranteed to work.  In particular, all existing 
    implementations do not support it."""
    def __init__(self):
        self._message_queue=[]
    def push_message(self,message):
        """Output a message.  This will not be displayed straight away, rather
        the full set until next user interaction will be accumulated (in what 
        I previously called a "sequester") until next user interaction and 
        then output with a -- More -- prompt."""
        self._message_queue.append(message)
    def slow_push_message(self,text):
        """Like push_message(...), but wrap to 60 chars.
        
        Blatantly not thread-safe."""
        for i in textwrap.wrap(text,60):
            self.push_message(i)
    def slow_ask_question(self,text):
        """Like ask_question(...), but wrap to 60 chars.
        
        Blatantly not thread-safe."""
        trailer=text[len(text.rstrip()):]
        wrap=textwrap.wrap(text,60)
        for i in wrap[:-1]:
            self.push_message(i)
        self.dump_messages() #Hopefully not needed.
        return self.ask_question(wrap[-1]+trailer)
    #
    @staticmethod
    def works_p():
        """-->true if implementation works on this platform and environment"""
        raise NotImplementedError("should be implemented by subclass")
    def dump_messages(self):
        """Flush messages to screen.  Normally there should be no need to use
        this as it is called automatically upon user interaction."""
        raise NotImplementedError("should be implemented by subclass")
    def ask_question(self,question):
        raise NotImplementedError("should be implemented by subclass")
    def goto_point(self,x,y):
        """Move the user cursor/focus to coords (x,y)."""
        raise NotImplementedError("should be implemented by subclass")
    def set_window_title(self,title):
        """Sets the window title.  As you would expect."""
        #Might not be implement*able* in all cases.
        #Exception should be caught by level module.
        raise NotImplementedError
    def get_key_event(self):
        """Return a keyboard event in WConio.getkey style."""
        raise NotImplementedError("should be implemented by subclass")
    def plot_tile(self,y,x,tile_id):
        """Plot a tile at a point."""
        raise NotImplementedError("should be implemented by subclass")
