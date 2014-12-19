from WindowsBackend import WindowsBackend
from WconioMixin import WconioMixin

class WconioWindowsBackend(WindowsBackend,WconioMixin):
    @staticmethod
    def works_p():
        try:
            import WConio
        except ImportError:
            return 0
        else:
            return 1