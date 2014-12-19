def _getsign(value):
    return value/abs(value)
def genliney(constant,varience,invarience):
    return zip([constant]*abs(invarience-varience),range(varience,invarience,_getsign(invarience-varience)))
def genlinex(constant,varience,invarience):
    return zip(range(varience,invarience,_getsign(invarience-varience)),[constant]*abs(invarience-varience))