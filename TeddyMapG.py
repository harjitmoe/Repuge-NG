from TeddyMapBase import TeddyMapBase

class TeddyMapG(TeddyMapBase):
    #Raw string (r""") because backslashes
    # Patio
    # Kitchen???  Study
    # Kitchen     Lounge
    coded_grid=r"""
/-------------------------------\
|...............................|
|...............................|
>------------T-T---T-----=------<
|............|.:...:............|
|............|&|...|............|
|............>-<...|............|
|............|.|...|............|
|............>-<...|,,,,,,,,,,,,|
|............|%|...|............|
|............|.|...|............|
|............|.|...|............|
|............:.....:............|
`------------^--=--^------------'
"""
    starting_pt=(16,13)
    title_window="The Verres' Ground Floor"
    def bring_to_front(self, playerobj, whence="unspecified"):
        if whence=="advancement":
            playerobj.place(14,6,self)
        elif whence=="regression":
            playerobj.place(14,10,self)
        else:
            playerobj.place(self.starting_pt[0],self.starting_pt[1],self)
    
    def handle_staircase(self,playerobj):
        if self.get_index_grid(*playerobj.pt)[1]=="%":
            self.game.level_advance(playerobj)
        else:
            self.game.level_regress(playerobj)
