__copying__="""
Written by Thomas Hori

This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/."""

class Saving(object):
    classmethod=classmethod
    staticmethod=staticmethod
    def _im(self):pass
    
    @staticmethod
    def strip_methods(d,also=()):
        d2={}
        for k in d.keys():
            if (not isinstance(d[k],Saving.meth)) and (k not in also) and (k[:2]!="__"):
                #print type(d[k])
                d2[k]=d[k]
        #print ("With also %r, yield keys %r"%(also,d2.keys()))
        return d2

Saving.instancemethod=type(Saving._im)
Saving.meth=(Saving.instancemethod,Saving.classmethod,Saving.staticmethod)