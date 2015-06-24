from GridObject import GridObject
class Container(GridObject):
    contents=None
    def initialise(self,play=None):
        self.contents=[]
    def insert(self,object):
        if object.status=="placed":
            object.lift()
        elif object.status=="contained":
            object.container.remove(object)
        elif object.status!="unplaced":
            raise ValueError("unheard-of object status %r"%object.status)
        #
        if object in self.contents:
            raise RuntimeError("unplaced object in container's inventory")
        self.contents.append(object)
        object.status="contained"
        object.container=self
    def remove(self,object):
        self.contents.remove(object)
        object.status="unplaced"
        object.container=None
    def drop(self,object,pt):
        self.remove(object)
        object.place(*pt)
    def dump(self,pt):
        for object in self.contents[:]:
            self.drop(object,pt)
    def level_rebase(self,newlevel):
        self.level=newlevel
        for i in self.contents:
            i.level=newlevel
