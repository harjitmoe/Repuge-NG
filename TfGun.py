from ludicrous.GridObject import GridObject
from TfBeam import TfBeam

class TfGun(GridObject):
    """A TF gun.
    """
    tile = "wand"
    name = "TF gun"
    appearance = "flashy gun-shaped device"
    def shoot(self, direction):
        pt = self.pt
        c = self.container
        while c:
            pt = c.pt
            c = c.container
        TfBeam(self.game).throw(direction, pt, self.level)
