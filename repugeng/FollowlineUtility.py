from repugeng.StaticClass import StaticClass

class FollowlineUtility(StaticClass):
    """Utility for generating lines for Level.followline(...)"""
    def _getsign(cls, value):
        return value/abs(value)
    def genliney(cls, constant, beginning, unto):
        """Return points for x = constant, beginning <= y < unto (or beginning >= y>unto)."""
        return zip([constant]*abs(unto-beginning),
                   range(beginning, unto, cls._getsign(unto-beginning)))
    def genlinex(cls, constant, beginning, unto):
        """Return points for y = constant, beginning <= x < unto (or beginning >= y>unto)."""
        return zip(range(beginning, unto, cls._getsign(unto-beginning)),
                   [constant]*abs(unto-beginning))
