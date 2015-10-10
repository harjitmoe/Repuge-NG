from consolation.DisplaySelector import DisplaySelector

display=DisplaySelector.get_display(False)
x=y=0
display.goto_point(x,y)

mode=0
line_top=0

textlines=[[]]

def redraw():
    for y,l in enumerate(textlines[line_top:][:20]):
        for x in range(80):
            display.plot_tile_ex(x,y,"space"," ")
        for x in range(len(l)):
            display.plot_tile_ex(x,y,"letter_"+l[x],l[x])

def redraw_line():
    l=textlines[y]
    for x in range(80):
        display.plot_tile_ex(x,y,"space"," ")
    for x in range(len(l)):
        display.plot_tile_ex(x,y,"letter_"+l[x],l[x])

fn="%"
def save(n):
    f=open(n,"w")
    f.write("\n".join(["".join(l) for l in textlines]))
    f.close()

def openf(n):
    global textlines
    global fn
    f=open(n,"rU")
    textlines=[list(l) for l in f.read().split("\n")]
    fn=n
    redraw()
    f.close()

nom=""
cn=""

while 1:
    key=display.get_key_event()
    if mode==0:
        if key in "0123456789":
            nom+=key
            continue
        else:
            cn=int("0"+nom,10)
            nom=""
        if key in ("h","left"):
            x-=1
            if x<0:
                x=0
        elif key in ("j","down"):
            y+=1
            if (line_top+y)>=len(textlines):
                y-=1
            elif y>20:
                line_top+=1
                y-=1
                redraw()
            while x>=len(textlines[line_top+y]):
                x-=1
            if x<0:
                x=0
        elif key=="+":
            y+=1
            if (line_top+y)>=len(textlines):
                y-=1
            elif y>20:
                line_top+=1
                y-=1
                redraw()
            x=0
        elif key in ("k","up"):
            y-=1
            if y<0:
                if line_top>0:
                    line_top-=1
                    redraw()
                y=0
            while x>=len(textlines[line_top+y]):
                x-=1
            if x<0:
                x=0
        elif key=="-":
            y-=1
            if y<0:
                if line_top>0:
                    line_top-=1
                    redraw()
                y=0
            x=0
        elif key in ("l","right"):
            x+=1
            if x>=len(textlines[line_top+y]):
                x-=1
        elif key=="i":
            mode=1
        elif key=="I":
            x=0
            mode=1
        elif key=="a":
            x+=1
            mode=1
        elif key=="A":
            x=len(textlines[line_top+y])
            mode=1
        elif key=="o":
            x=0
            y+=1
            textlines.insert(y,[])
        elif key=="O":
            x=0
            textlines.insert(y,[])
        elif key=="d":
            mode=2
        elif key=="|":
            x=cn
            while x>=len(textlines[line_top+y]):
                x-=1
            if x<0:
                x=0
        elif key=="^":
            x=0
        elif key=="$":
            x=len(textlines[line_top+y])-1
        elif key==":":
            arg=display.ask_question(":").split(" ",1)
            if arg:
                cmd=arg.pop(0)
                if cmd=="w":
                    if not arg:
                        n=fn
                    else:
                        n=arg[0]
                    save(n)
                elif cmd=="e":
                    if not arg:
                        textlines=[[]]
                        y=x=0
                        redraw()
                    else:
                        n=arg[0]
                        openf(n)
                elif cmd=="x":
                    save(fn)
                    raise SystemExit(0)
                elif cmd=="q":
                    raise SystemExit(0)
    elif mode==1: #insert mode
        if key=="\x1b": #The escape key
            mode=0
            if x>=len(textlines[line_top+y]):
                x-=1
        elif key in "\r\n": #See what I did there?
            x=0
            y+=1
            textlines.insert(y,[])
            if y>20:
                line_top+=1
                y-=1
                redraw()
        elif key in "\b\x1f":
            x-=1
            if x<0:
                x=0
            else:
                del textlines[line_top+y][x]
                redraw_line()
        else:
            textlines[line_top+y].insert(x,key[:1])
            redraw_line()
            x+=1
    elif mode==2: #deletion mode
        if key=="d":
            del textlines[line_top+y]
            if (line_top+y)>=len(textlines):
                y-=1
        #XXX
    display.goto_point(x,y)
