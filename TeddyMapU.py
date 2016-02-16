from TeddyMapBase import TeddyMapBase
from OwlObject import OwlObject

class TeddyMapU(TeddyMapBase):
    #Raw string (r""") because backslashes
    # Grace  Bathroom
    # Tedd   Edward
    # (or a 360deg rotation thereof)
    coded_grid=r"""



/------------T-----T------------\
|............|.....|............|
|............:.....:............|
|............|.....|............|
|............|.|...|............|
>------------<.|...>------------<
|............|&|...|............|
|............>-'...|............|
|............:.....:............|
|............|.....|............|
`------------^-----^------------'
"""
    starting_pt=(14,10)
    title_window="The Verres' House Upstairs"
  
    def handle_staircase(self,playerobj):
        self.game.level_regress(playerobj)

    def initialise(self):
        #Place owl
        self.owl=OwlObject(self.game)
        x,y=self.get_new_point()
        self.owl.place(x,y,self)
