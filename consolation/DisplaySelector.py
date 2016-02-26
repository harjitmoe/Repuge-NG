import os
from consolation.PosixDisplay import PosixDisplay
from consolation.WConioDisplay import WConioDisplay
from consolation.RpcDisplay import RpcDisplay
from consolation.StaticClass import StaticClass

__copying__="""
Written by Thomas Hori

This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/."""

class DisplaySelector(StaticClass):
    dispatcher = {"nt": [WConioDisplay, RpcDisplay], "posix": [PosixDisplay, RpcDisplay]}
    @classmethod #Keeps pylint happy
    def get_display(cls, rpc=True):
        """Obtain an instance implementing the Display API.

        rpc is True, False or -1:

        * True: use it
        * False: don't use it if possible
        * -1: this *is* the remote, so definitely not!
        """
        if rpc and (rpc > 0):
            return RpcDisplay()
        for i in cls.dispatcher[os.name]:
            if ((not rpc) or i != RpcDisplay) and i.works_p():
                if i == RpcDisplay:
                    print ("No supported local backend, " #pylint: disable = superfluous-parens
                           "falling back to RPC.")
                    print ("(On Windows, WConio is " #pylint: disable = superfluous-parens
                           "required due to the lack of ANSI escapes.)")
                return i()
        raise ImportError("no supported backend.  On Windows, install WConio.")
