class Backend(object):
    """Partially implementing base class"""
    def __init__(self):
        self._message_queue=[]
    def push_message(self,message):
        self._message_queue.append(message)
    #
    @staticmethod
    def works_p():
        return 0 #Base class, no it doesn't "work"
    def dump_messages(self):
        raise NotImplementedError,"should be implemented by subclass"
    def ask_question(self,question):
        raise NotImplementedError,"should be implemented by subclass"
    def goto_point(self,x,y):
        raise NotImplementedError,"should be implemented by subclass"
    def set_window_title(self,title):
        #Might not be implement*able* in all cases.
        #Exception should be caught by level module.
        raise NotImplementedError
    def get_key_event(self):
        raise NotImplementedError,"should be implemented by subclass"
    def plot_tile(self,y,x,tile_id):
        raise NotImplementedError,"should be implemented by subclass"
