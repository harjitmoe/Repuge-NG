from ludicrous.GridObject import GridObject

class TfBeam(GridObject):
    """A beam from a TF gun.
    """
    tile = "projectile"
    name = "TF-gun beam"
    appearance = "beam of green light"
    tangible = 0
    #XXX override hit(...)
