__copying__="""
This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/."""

class _StaticClassMetaclass(type): #How badass...
    """Metaclass of StaticClass."""
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
# supports the other's syntax, but both support class constructors.

# Define class methods here, not as instance methods on the metaclass,
# to make pylint shut up.
#
class StaticClass(_StaticClass):
    """Static class: a class not intended to have instances.

    Methods are automatically bound as class methods.

    _StaticClassMetaclass is the metaclass, and is not
    accessible directly, whereas StaticClass is an instance
    of that metaclass (and therefore a class) and should be
    inherited from.
    """
    @classmethod
    def _cascade_method(cls, method, *args, **kwargs):
        """Manage cascading inheritance of methods."""
        # Simple MRO, will do.
        bases=[cls]
        while bases:
            cls2=bases.pop(0)
            bases.extend(cls2.__bases__)
            if hasattr(cls2, method):
                r=getattr(cls2, method)(*args,**kwargs)
                if r!=None:
                    return r
        return None

del _StaticClass
del _StaticClassMetaclass
