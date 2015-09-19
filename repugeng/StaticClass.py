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

_StaticClass = _StaticClassMetaclass("StaticClass", (object,), {})

# As for why I'm not using 2k __metaclass__ or 3k metaclass=, neither
# supports the other's syntax, but both support the Don Beaudry hook,
# (used above) which was made available for pure-Python (then classic)
# classes back in Python 1.5, having been available earlier via C.
# Accordingly, it was usable before new-style classes even existed,
# and was perfectly usable for new-style classes from the get-go, and
# still is entirely usable in  3k.

# Define class methods here, not as instance methods on the metaclass,
# to make pylint shut up.
#
class StaticClass(_StaticClass):
    @classmethod
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

del _StaticClass
del _StaticClassMetaclass
