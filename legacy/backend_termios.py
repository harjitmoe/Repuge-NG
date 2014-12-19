import sys,termios
mapoftiles={
    "space":" ",
    "vwall":         "\x1b[1;31m|",
    "hwall":         "\x1b[1;31m-",
    "wall_corner_nw":"\x1b[1;31m-", #In true Rogue style
    "wall_corner_ne":"\x1b[1;31m-", #In true Rogue style
    "wall_corner_sw":"\x1b[1;31m-", #In true Rogue style
    "wall_corner_se":"\x1b[1;31m-", #In true Rogue style
    "wall_TeeJnc_up":"\x1b[1;31m-", #In true continuation of Rogue style
    "wall_TeeJnc_dn":"\x1b[1;31m-", #In true continuation of Rogue style
    "wall_TeeJnc_rt":"\x1b[1;31m|", #In true continuation of Rogue style
    "wall_TeeJnc_lt":"\x1b[1;31m|", #In true continuation of Rogue style
    "wall_cross":    "\x1b[1;31m-", #In true continuation of Rogue style
##If you can get it to output OEM try using these!
#    "vwall":"\x1b[1;31m\xb3",
#    "hwall":"\x1b[1;31m\xc4",
#    "wall_corner_nw":"\x1b[1;31m\xda",
#    "wall_corner_ne":"\x1b[1;31m\xbf",
#    "wall_corner_sw":"\x1b[1;31m\xc0",
#    "wall_corner_se":"\x1b[1;31m\xd9",
#    "wall_TeeJnc_up":"\x1b[1;31m\xc1",
#    "wall_TeeJnc_dn":"\x1b[1;31m\xc2",
#    "wall_TeeJnc_rt":"\x1b[1;31m\xc3",
#    "wall_TeeJnc_lt":"\x1b[1;31m\xb4",
#    "wall_cross":"\x1b[1;31m\xc5",
    "vfeature":"\x1b[1;31m:",
    "hfeature":"\x1b[1;31m=",
    #Levels of floor
    "floor1":"\x1b[1;30m.",
    "floor2":"\x1b[1;30m,",
    "floor3":"\x1b[1;30m/",
    "floor4":"\x1b[1;30m$",
    "floor5":"\x1b[1;30m#",
    "user":"\x1b[22;37m@",
    "fred":"\x1b[22;37m@",
    "ron":"\x1b[22;37m@",
    "hermione":"\x1b[22;37m@",
    "quirrel":"\x1b[22;37m@",
    "peeves":"\x1b[22;37mP",
    "malfoy":"\x1b[22;37mM",
    "crabbe":"\x1b[22;37m@",
    "goyle":"\x1b[22;37m@",
    "quirrel":"\x1b[22;37m@",
    "gnome":"\x1b[22;37mG",
    "flitwick":"\x1b[22;37m@",
    "snail":"\x1b[22;37mS",
    "tent":"\x1b[22;37mT",
    "tentacle":"\x1b[22;37m~",
    "sprout":"\x1b[22;37m@",
    "bush":"\x1b[22;37mB",
    "needle":"\x1b[22;37m~",
    "chest":"\x1b[22;37m]",
    "cauldron":"\x1b[22;37m)",
    "doxy":"\x1b[22;37mD",
    "snare":"\x1b[22;37ms",
    "boulder":"\x1b[22;37mO",
    "snape":"\x1b[22;37m@",
    "ingredient":"\x1b[22;37m%",
    "filtch":"\x1b[22;37m@",
    "norris":"\x1b[22;37m&",
    "fluffyhead":"\x1b[22;37m+",
    "erised":"\x1b[22;37m}",
    "dumbledore":"\x1b[22;37m@",
    "bean":"\x1b[22;37m'",
    "card":'\x1b[22;37m"',
    "frog":"\x1b[22;37mf",
    "extra":"\x1b[22;37m@",
    "drink":"\x1b[22;37m!",
}

plotcache={}#Needed as flushing ansi escapes seems to take time
def plot(y,x,c):
    c=mapoftiles[c]
    if ((y,x) not in plotcache) or (plotcache[(y,x)]!=c):
        sys.stderr.write("\x1B[?25l") #hide cursor, ? means extension, and that's a lowercase L
        sys.stderr.write("\x1B[%d;%dH%s"%(y+1,x+1,c))
        sys.stderr.write("\x1B[m") #reset colour
        sys.stderr.write("\x1B[?25h") #show cursor, ? means extension
        sys.stderr.flush()
        plotcache[(y,x)]=c
    gotopt(*pt)

#Goto point: calling a function goto is a dumb idea even in Python in case
#someone extends the syntax (though unlikely)
pt=[0,0]
def gotopt(x,y):
    pt[:]=x,y
    sys.stderr.write("\x1B[%d;%dH"%(y+1,x+1))

def title(text):
    sys.stderr.write("\x1b]0;%s\x1b\\"%text)

def _getch(reset_afterwards=0): #avoid misechoed keystrokes between checks
    attrs=termios.tcgetattr(0);
    termios.tcsetattr(0,termios.TCSADRAIN,attrs[:3]+[attrs[3]&(~termios.ICANON)&(~termios.ECHO)]+attrs[4:])
    termios.tcdrain(0)
    char=sys.stdin.read(1)
    if reset_afterwards:
        termios.tcsetattr(0,termios.TCSADRAIN,attrs)
    return char

def _reset_terminal():
    attrs=termios.tcgetattr(0);
    termios.tcsetattr(0,termios.TCSADRAIN,attrs[:3]+[attrs[3]|termios.ICANON|termios.ECHO]+attrs[4:])
    termios.tcdrain(0)

def getkeyevent():
    global plotcache
    #plotcache={} #Get rid o_reset_terminal()f the misechoed keystrokes
    s=_getch()
    #outputtext(`s`)
    if s=="\x1b":
        s=_getch()
        #outputtext(`s`)
        if s=="[":
            s=_getch()
            #outputtext(`s`)
            if s=="A":
                s="up"
            elif s=="B":
                s="down"
            elif s=="C":
                s="right"
            elif s=="D":
                s="left"
    return s

bufz=["","",""]
def outputtext(s):
    while len(s)<79:
        s+=" "
    bufz.append(s)
    bufz.pop(0)
    oldpt=pt[:]
    gotopt(0,19)
    sys.stderr.write("\x1b[1;37m")
    for i in bufz:
        sys.stderr.write(i+"\n")
    sys.stderr.write("\x1b[m") #reset colour
    sys.stderr.flush()
    sys.stderr.write("\x1b[1;37m")
    gotopt(*oldpt)
def querytext(s):
    bufz.pop(0)
    oldpt=pt[:]
    gotopt(0,19)
    for i in bufz:
        print(i)
    print(" "*79)
    gotopt(0,21)
    _reset_terminal()
    returndat=raw_input(s)
    s=s+returndat
    while len(s)<79:
        s+=" "
    bufz.append(s)
    gotopt(0,19)
    for i in bufz:
        print(i)
    gotopt(*oldpt)
    return returndat

#Because this is Linux it behooveth thee (thou?) to clear the screen first
print("\x1b[2J")
