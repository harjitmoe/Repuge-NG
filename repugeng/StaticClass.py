class _StaticClassMetaclass(type): #How badass...
    """Static class: a class not intended to have instances.

    Methods are automatically bound as class methods.

    _StaticClassMetaclass is the metaclass, and is not
    accessible directly, whereas StaticClass is an instance
    of that metaclass (and therefore a class) and should be
    inherited from.
    """
    def __new__(mcs, name, bases, attrs):
        """Override __new__ to default to bound class methods,
        not to unbound instance methods."""
        for key in attrs:
            if isinstance(attrs[key], type(lambda:None)):
                attrs[key] = classmethod(attrs[key])
        cls=type.__new__(mcs, name, bases, attrs)
        return cls
    def __call__(cls):
        """Raise an error if anyone erroneously tries to
        create an instance of this static class."""
        raise TypeError("attempt to create instance of static class")
    def _cascade_method(cls, method, errors, *args, **kwargs):
        """Manage cascading inheritance of methods."""
        # Not one of Python's algorithms (see "What's New in Python 2.2"
        # for those ones) but it will do.
        bases=[cls]
        while bases:
            cls2=bases.pop(0)
            bases.extend(cls2.__bases__)
            if hasattr(cls2, method):
                r=getattr(cls2, method)(*args,**kwargs)
                if r not in errors:
                    return r
        return errors[0]

StaticClass = _StaticClassMetaclass("StaticClass", (object,), {})
del _StaticClassMetaclass
