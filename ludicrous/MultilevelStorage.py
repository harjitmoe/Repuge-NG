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
    #__dict__["42"] = {} set at end of file
    def __new__(cls, name):
        if name in getattr(cls,"42"):
            return getattr(cls,"42")[name]
        else:
            novus = object.__new__(cls)
            getattr(cls,"42")[name] = novus
            setattr(novus,"42",None) #Cannot del, but still break ref to keep mutable dict safer
            return novus
    def initialise_property(self, name, value):
        """Initialise an attribute to a value without overwriting
        any existing value.

        Behaviour in case of non-valid names is undefined and
        may be influenced by implementation details.
        """
        if not hasattr(self, name):
            self.__dict__[name] = value
#
setattr(MultilevelStorage,"42",{})
