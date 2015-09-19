from repugeng.StaticClass import StaticClass
import sys

class Compat3k(StaticClass):
    @classmethod
    def str_to_bytes(cls, s):
        """Convert a string of either width to a byte string."""
        try:
            try:
                return bytes(s)
            except NameError:
                return str(s)
        except ValueError:
            pass #Not ASCII?  Not really a problem...
        except TypeError:
            pass #I didn't specify an encoding?  Oh, boo hoo...
        return s.encode("latin1") #Not utf-8, m'kay...
    @classmethod
    def prompt_user(cls, s="", file=None):
        """Substitute of py2k's raw_input()."""
        (file or sys.stderr).write(s)
        return sys.stdin.readline().rstrip("\r\n")
