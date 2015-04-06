from repugeng.Level import Level

class PregenLevel(Level):
    gamut=None
    nsiz=0
    def initmap(self):
        self.genmap()
    def genmap(self):
        raise NotImplementedError
