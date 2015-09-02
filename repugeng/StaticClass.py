class _StaticClassMetaclass(type): #How badass...
    """Static class: a class not intended to have instances.

    Instance methods are automatically made into class methods."""
    def __new__(cls,name,bases,attrs):
        classify={}
        for key in attrs:
            if isinstance(attrs[key],type(lambda:None)):
                attrs[key]=classmethod(attrs[key])
        self=type.__new__(cls,name,bases,attrs)
        return self
    def __call__(self):
        """Raise an error if anyone tries to erroneously create an instance of
        this static class."""
        raise TypeError("attempt to create instance of static class")

StaticClass=_StaticClassMetaclass("StaticClass",(object,),{})
del _StaticClassMetaclass
