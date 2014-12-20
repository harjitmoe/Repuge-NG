class MultilevelStorage(object):
    existing={}
    @staticmethod
    def __new__(cls,name):
        if name in cls.existing:
            return cls.existing[name]
        else:
            new=object.__new__(cls)
            cls.existing[name]=new
            new.existing=None #Cannot del, but still break ref to keep mutable dict safer
            return new
