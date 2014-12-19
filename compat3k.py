#3k compatibility measures
try:
    bytes=bytes
except NameError:
    bytes=str
else:
    def bytes(x):
        return x.encode("latin1") #as in not utf8?
try:
    raw_input=raw_input
except NameError:
    def raw_input(x):
        #2x raw_input() is ironically less raw that 3k input()
        return input(x).rstrip("\r")


