#3k compatibility measures
try:
    bytes=bytes #pylint: disable=redefined-builtin
except NameError:
    bytes=str #pylint: disable=redefined-builtin
else:
    bytes=lambda x: x.encode("latin1") #pylint: disable=redefined-builtin
try:
    raw_input=raw_input #pylint: disable=redefined-builtin
except NameError:
    raw_input=lambda x: input(x).rstrip("\r\n") #pylint: disable=redefined-builtin,bad-builtin


