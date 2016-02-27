from ludicrous.GridObject import GridObject
from OwlObject import OwlObject

class TfBeam(GridObject):
    """A beam from a TF gun.
    """
    tile = "projectile"
    name = "TF-gun beam"
    appearance = "beam of green light"
    tangible = 0
    def hit(self, obj, projector=None):
        if hasattr(obj, "myinterface") and obj.myinterface != None:
            # obj is the player
            if type(self) in obj.known: #pylint: disable = unidiomatic-typecheck
                obj.myinterface.push_message("The %s hits!"%self.name)
            else:
                obj.myinterface.push_message("The %s hits!"%self.appearance)
        for aninterface in self.level.child_interfaces:
            playerobj = aninterface.playerobj
            if playerobj == obj:
                continue #The victim was already notified
            if type(self) in playerobj.known: #pylint: disable = unidiomatic-typecheck
                myname=self.name
            else:
                myname=self.appearance
            if type(obj) in playerobj.known: #pylint: disable = unidiomatic-typecheck
                objname=obj.name
            else:
                objname=obj.appearance
            aninterface.push_message("The %s hits the %s!"%(myname, objname))
        obj.polymorph(OwlObject)
