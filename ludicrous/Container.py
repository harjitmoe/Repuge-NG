from ludicrous.GridObject import GridObject
class Container(GridObject):
    contents = None
    def initialise(self):
        self.contents = []
    def insert(self, obj):
        if obj.status == "placed":
            obj.lift()
        elif obj.status == "contained":
            obj.container.remove(obj)
        elif obj.status != "unplaced":
            raise ValueError("unheard-of obj status %r"%obj.status)
        #
        if obj in self.contents:
            raise RuntimeError("unplaced obj in container's inventory")
        self.contents.append(obj)
        obj.status = "contained"
        obj.container = self
    def remove(self, obj):
        self.contents.remove(obj)
        obj.status = "unplaced"
        obj.container = None
    def drop(self, obj, pt):
        self.remove(obj)
        obj.place(*pt)
    def dump(self, pt):
        for obj in self.contents[:]:
            self.drop(obj, pt)
    def level_rebase(self, newlevel):
        self.level = newlevel
        for i in self.contents:
            i.level = newlevel
