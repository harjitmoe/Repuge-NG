class MultilevelStorage(object):
    """An object enabling storage across levels.

    Is called with a hashable object, normally a string, identifying
    the object uniquely.  If class is initialised with the same
    identifier, a reference to the selfsame object will be returned,
    with all changes made by any previous level.

    Use initialise_property(...) to initialise an attribute to a
    value without overwriting any existing value.  Caveat: this does
    not work properly for any attribute called "existing" due to
    implementation details, it is not recommended to use a attribute
    by that name.
    """
    existing = {}
    def __new__(cls, name):
        if name in cls.existing:
            return cls.existing[name]
        else:
            novus = object.__new__(cls)
            cls.existing[name] = novus
            novus.existing = None #Cannot del, but still break ref to keep mutable dict safer
            return novus
    def initialise_property(self, name, value):
        """Initialise an attribute to a value without overwriting
        any existing value.

        Caveat: this does not work properly for any attribute
        called "existing" due to implementation details, it is
        not recommended to use a attribute by that name.
        """
        if not hasattr(self, name):
            self.__dict__[name] = value
