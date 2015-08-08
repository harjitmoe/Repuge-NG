class FollowlineUtility(object):
    """Utility for generating lines for Level.followline(...)"""
    @staticmethod
    def __new__(cls,*a,**kw):
        raise TypeError("attempt to create instance of static class")
    #
    @staticmethod
    def _getsign(value):
        return value/abs(value)
    @classmethod
    def genliney(cls,constant,beginning,unto):
        """Return points for x=constant, beginning<=y<unto (or beginning>=y>unto)."""
        return zip([constant]*abs(unto-beginning),range(beginning,unto,cls._getsign(unto-beginning)))
    @classmethod
    def genlinex(cls,constant,beginning,unto):
        """Return points for y=constant, beginning<=x<unto (or beginning>=y>unto)."""
        return zip(range(beginning,unto,cls._getsign(unto-beginning)),[constant]*abs(unto-beginning))