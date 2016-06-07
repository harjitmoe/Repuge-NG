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
        print ("With also %r, yield keys %r"%(also,d2.keys()))
        return d2

Saving.instancemethod=type(Saving._im)
Saving.meth=(Saving.instancemethod,Saving.classmethod,Saving.staticmethod)