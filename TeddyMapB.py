from TeddyMapBase import TeddyMapBase
from TfGun import TfGun

class TeddyMapB(TeddyMapBase):
    #Raw string (r""") because backslashes
    # Lab  "Other room"
    coded_grid=r"""



/------------T-T----------------\
|............>-<................|
|............|%|................|
|............|.|................|
|............|.|................|
|..............|................|
|..............|................|
|...............................|
|...............................|
|...............................|
`--------------^----------------'
"""
    starting_pt=(14,6)
    title_window="The Verres' Basement"
    
    def handle_staircase(self,playerobj):
        self.game.level_advance(playerobj)

    def initialise(self):
        #Place TF-gun
        self.gun=TfGun(self.game)
        x,y=self.get_new_point()
        self.gun.place(x,y,self)
