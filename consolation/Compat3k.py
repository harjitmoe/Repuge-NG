from consolation.StaticClass import StaticClass
import sys

__copying__="""
Written by Thomas Hori

This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/."""

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
        (file or sys.stderr).flush()
        return sys.stdin.readline().rstrip("\r\n")
