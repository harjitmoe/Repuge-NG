import sys
from repugeng.Backend import Backend
from repugeng.ConsoleTiles import ConsoleTiles
from repugeng.compat3k import *

class ConsoleBackend(Backend):
    """Partially implementing base class"""
    _tiles_class=ConsoleTiles
    def __init__(self,*a,**kw):
        self._messages_visible=["","",""]
        self.point=[0,0]
        super(ConsoleBackend,self).__init__(*a,**kw)
    def _output_text(self,i):
        sys.stderr.write(i)
        sys.stderr.flush() #breaks on 3.1 on win32 otherwise
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
    def plot_tile(self,x,y,tile_id):
        return self._plot_character(x,y,self._tiles_class.get_tile_character(tile_id))
    def attach_expansion_pack(self,pack):
        self._tiles_class.attach_expansion_pack(pack)
    #
    def _plot_character(self,x,y,c):
        raise NotImplementedError("should be implemented by subclass")
    def _put_to_message_area(self,s,ask,s2=None,collect_input=1):
        """The backend behind all putting to the console message area, 
        for ask or say.
        
        Not thread safe.

        Arguments:
        - s: The string to output.
        - ask: Boolean, should user input be collected?
        - s2: String for in-place change of question after user input collected.
          This should ONLY be used for removing -- More -- prompts and the like, 
          which should not be kept around in the message log.
        - collect_input: Boolean, should the user input be collected?  Keep as 1
          unless the user is supposed to acknowledge receipt of the message with
          Return but not actually supposed to input stuff (e.g. More prompt).
        """
        if s2==None:
            s2=s
        self._engage_message_formatting()
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
            if (not collect_input):
                self._output_text(s)
                #Wait for key event without triggering recursion.
                #XXX kluge, not thread safe.
                bkq,self._message_queue=self._message_queue,[]
                self.get_key_event()
                self._message_queue=bkq+self._message_queue
                s=s2
            else:
                returndat=raw_input(s)
                s=s2
                s=s+returndat
        while len(s)<79:
            s+=" "
        self._messages_visible.append(s)
        self.goto_point(0,19)
        for i in self._messages_visible:
            self._output_text(i+"\n")
        self._end_message_formatting()
        self.goto_point(*old_point)
        if collect_input:
            return returndat
