class FollowlineUtility(object):
    """Utility for generating lines for followline(...) and followline_user(...)"""
    @staticmethod
    def __new__(cls,*a,**kw):
        raise TypeError("attempt to create instance of static class")
    #
    @staticmethod
    def _getsign(value):
        return value/abs(value)
    @classmethod
    def genliney(cls,constant,varience,invarience):
        """Return points for x=constant, varience<=y<invarience (or varience>=y>invarience).
        
        Starting, that is, at (constant,varience).
        
        ... am I that bad at parameter naming?"""
        return zip([constant]*abs(invarience-varience),range(varience,invarience,cls._getsign(invarience-varience)))
    @classmethod
    def genlinex(cls,constant,varience,invarience):
        """Return points for y=constant, varience<=x<invarience (or varience>=y>invarience).
        
        Starting, that is, at (varience,constant).
        
        ... am I that bad at parameter naming?"""
        return zip(range(varience,invarience,cls._getsign(invarience-varience)),[constant]*abs(invarience-varience))