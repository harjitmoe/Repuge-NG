import textwrap

class Backend(object):
    """Partially implementing base class"""
    def __init__(self):
        self._message_queue=[]
    def push_message(self,message):
        self._message_queue.append(message)
    def slow_push_message(self,text):
        for i in textwrap.wrap(text,60):
            self.push_message(i)
    def slow_ask_question(self,text):
        trailer=text[len(text.rstrip()):]
        wrap=textwrap.wrap(text,60)
        for i in wrap[:-1]:
            self.push_message(i)
        self.dump_messages() #Hopefully not needed.
        return self.ask_question(wrap[-1]+trailer)
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
