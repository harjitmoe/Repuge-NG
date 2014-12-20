class UtilityMethods(object):
    @staticmethod
    def __new__(cls,*a,**kw):
        raise TypeError("attempt to create instance of static class")
    #
    @staticmethod
    def _getsign(value):
        return value/abs(value)
    @classmethod
    def genliney(cls,constant,varience,invarience):
        return zip([constant]*abs(invarience-varience),range(varience,invarience,cls._getsign(invarience-varience)))
    @classmethod
    def genlinex(cls,constant,varience,invarience):
        return zip(range(varience,invarience,cls._getsign(invarience-varience)),[constant]*abs(invarience-varience))