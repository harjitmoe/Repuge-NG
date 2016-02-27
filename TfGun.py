from ludicrous.GridObject import GridObject
from TfBeam import TfBeam

class TfGun(GridObject):
    """A TF gun.
    """
    tile = "wand"
    name = "TF gun"
    appearance = "flashy gun-shaped device"
    def zap(self, direction, pt, level):
        TfBeam(self.game).throw(direction, pt, level, self)
