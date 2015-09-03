from repugeng.StaticClass import StaticClass

class FollowlineUtility(StaticClass):
    """Utility for generating lines for Level.followline(...)"""
    @classmethod #Keeps pylint happy
    def _getsign(cls, value):
        """Return -1 for a negative number or 1 for a positive number."""
        return value/abs(value)
    @classmethod #Keeps pylint happy
    def genliney(cls, constant, beginning, unto):
        """Return points for x = constant, beginning <= y < unto (or beginning >= y>unto)."""
        return zip([constant]*abs(unto-beginning),
                   range(beginning, unto, cls._getsign(unto-beginning)))
    @classmethod #Keeps pylint happy
    def genlinex(cls, constant, beginning, unto):
        """Return points for y = constant, beginning <= x < unto (or beginning >= y>unto)."""
        return zip(range(beginning, unto, cls._getsign(unto-beginning)),
                   [constant]*abs(unto-beginning))
