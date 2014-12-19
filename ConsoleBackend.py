import sys
from Backend import Backend
from ConsoleTiles import ConsoleTiles
from compat3k import *

class ConsoleBackend(Backend):
    """Partially implementing base class"""
    _tiles_class=ConsoleTiles
    def __init__(self,*a,**kw):
        self._messages_visible=["","",""]
        self.point=[0,0]
        super(ConsoleBackend,self).__init__(*a,**kw)
    def _output_text(self,i):
        sys.stderr.write(i)
    def _engage_message_formatting(self):
        pass
    def _end_message_formatting(self):
        pass
    def _reset_terminal(self):
        pass #Subclasses to only implement if actually needed
    def dump_messages(self):
        if self._message_queue:
            while self._message_queue[1:]:
                line=self._message_queue.pop(0)
                self._put_to_message_area(line+" -- More -- ",1,line,0)
            self._put_to_message_area(self._message_queue.pop(),0)
    def ask_question(self,s):
        self.dump_messages()
        return self._put_to_message_area(s,1)
    def plot_tile(self,y,x,tile_id):
        return self._plot_character(y,x,self._get_tile_character(tile_id))
    #
    def _plot_character(self,y,x,c):
        raise NotImplementedError,"should be implemented by subclass"
    def _get_tile_character(self,tile_id):
        return getattr(self._tiles_class,tile_id)
    def _put_to_message_area(self,s,ask,s2=None,re_echo_input=1):
        """The backend behind all putting to the message area, for ask or say."""
        if s2==None:
            s2=s #idea is that s2 does not contain -- More -- where applicable
        self._messages_visible.pop(0)
        old_point=self.point[:]
        returndat=None
        if ask:
            self.goto_point(0,19)
            for i in self._messages_visible:
                self._output_text(i+"\n")
            self._output_text(" "*79+"\n")
            self.goto_point(0,21)
            self._reset_terminal()
            returndat=raw_input(s)
            s=s2
            if re_echo_input:
                s=s+returndat
        while len(s)<79:
            s+=" "
        self._messages_visible.append(s)
        self.goto_point(0,19)
        if not ask: self._engage_message_formatting()
        for i in self._messages_visible:
            self._output_text(i+"\n")
        if not ask: self._end_message_formatting()
        self.goto_point(*old_point)
        return returndat
    