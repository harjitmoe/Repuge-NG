import WConio
mapoftiles={
    "space":" ",
#    "vwall":"|",
#    "hwall":"-",
#    "wall_corner_nw":"-", #In true Rogue style
#    "wall_corner_ne":"-", #In true Rogue style
#    "wall_corner_sw":"-", #In true Rogue style
#    "wall_corner_se":"-", #In true Rogue style
#    "wall_TeeJnc_up":"-", #In true continuation of Rogue style
#    "wall_TeeJnc_dn":"-", #In true continuation of Rogue style
#    "wall_TeeJnc_rt":"|", #In true continuation of Rogue style
#    "wall_TeeJnc_lt":"|", #In true continuation of Rogue style
#    "wall_cross":"-", #In true continuation of Rogue style
    "vwall":"\xb3",
    "hwall":"\xc4",
    "wall_corner_nw":"\xda",
    "wall_corner_ne":"\xbf",
    "wall_corner_sw":"\xc0",
    "wall_corner_se":"\xd9",
    "wall_TeeJnc_up":"\xc1",
    "wall_TeeJnc_dn":"\xc2",
    "wall_TeeJnc_rt":"\xc3",
    "wall_TeeJnc_lt":"\xb4",
    "wall_cross":"\xc5",
    "vfeature":":",
    "hfeature":"=",
    #Levels of floor
    "floor1":".",
    "floor2":",",
    "floor3":"/",
    "floor4":"$",
    "floor5":"#",
#    "user":"@",
#    "fred":"@",
#    "ron":"@",
#    "hermione":"@",
#    "quirrel":"@",
    "user":"\x01",
    "fred":"\x02",
    "ron":"\x02",
    "hermione":"\x02",
    "quirrel":"\x02",
    "peeves":"P",
    "malfoy":"M",
#    "crabbe":"@",
#    "goyle":"@",
#    "quirrel":"@",
    "crabbe":"\x02",
    "goyle":"\x02",
    "quirrel":"\x02",
    "gnome":"G",
    "flitwick":"@",
    "snail":"S",
    "tent":"T",
    "tentacle":"~",
#    "sprout":"@",
    "sprout":"\x02",
    "bush":"B",
    "needle":"~",
    "chest":"]",
    "cauldron":")",
    "doxy":"D",
    "snare":"s",
    "boulder":"O",
#    "snape":"@",
    "snape":"\x02",
    "ingredient":"%",
#    "filtch":"@",
    "filtch":"\x02",
    "norris":"&",
    "fluffyhead":"+",
    "erised":"}",
#    "dumbledore":"@",
    "dumbledore":"\x02",
    "bean":"'",
    "card":'"',
    "frog":"f",
#    "extra":"@",
    "extra":"\x02",
    "drink":"!",
}

try:
    bytes=bytes
except NameError:
    bytes=str
else:
    def bytes(x):
        return x.encode("latin1")

try:
    raw_input=raw_input
except NameError:
    def raw_input(x):
        """Ironically less raw that input() in 3k"""
        return input(x).rstrip("\r")

def plot(x,y,c):
    c=mapoftiles[c]
    WConio.puttext(y,x,y,x,bytes(c+"\x07"))

#Goto point: calling a function goto is a dumb idea even in Python in case
#someone extends the syntax (though unlikely)
pt=[0,0]
def gotopt(x,y):
    pt[:]=x,y
    WConio.gotoxy(x,y)

def title(text):
    WConio.settitle(bytes(text))

def getkeyevent():
    return WConio.getkey()

bufz=["","",""]
def outputtext(s):
    while len(s)<79:
        s+=" "
    bufz.append(s)
    bufz.pop(0)
    oldpt=pt[:]
    gotopt(0,21)
    for i in bufz:
        print(i)
    gotopt(*oldpt)
def querytext(s):
    bufz.pop(0)
    oldpt=pt[:]
    gotopt(0,21)
    for i in bufz:
        print(i)
    print(" "*79)
    gotopt(0,23)
    returndat=raw_input(s)
    s=s+returndat
    while len(s)<79:
        s+=" "
    bufz.append(s)
    gotopt(0,21)
    for i in bufz:
        print(i)
    gotopt(*oldpt)
    return returndat
