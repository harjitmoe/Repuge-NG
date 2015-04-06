from repugeng.PregenLevel import PregenLevel
import random,math

class SimpleDungeonLevel(PregenLevel):
    """Level subclass for a simple rogue-like dungeon.

    Simple in that at will always contain rooms connected in a ring."""
    list_of_symbols={"g":"wall_corner_nw","G":"wall_corner_ne","j":"wall_corner_sw","J":"wall_corner_se","d":"vwall","o":"hwall",":":"vfeature","*":"vfeature"," ":"space",".":"floor1",",":"floor2","/":"floor3","$":"floor4","#":"floor5","P":"hfeature","l":"hfeature","v":"wall_TeeJnc_dn","^":"wall_TeeJnc_up",">":"wall_TeeJnc_rt","<":"wall_TeeJnc_lt","+":"wall_cross",}
    def _add_blocks_x(self,block1r,block2r,block3r):
        block1,gamut1=block1r
        b1w=len(block1.split("\n",1)[0])
        block2,gamut2=block2r
        b2w=len(block2.split("\n",1)[0])
        block3,gamut3=block3r
        block4=[]
        for line1,line2,line3 in zip(block1.split("\n"),block2.split("\n"),block3.split("\n")):
            block4.append(line1+line2+line3)
        return "\n".join(block4),gamut1+tuple((i[0]+b1w,i[1]) for i in gamut2)+tuple((i[0]+b1w+b2w,i[1]) for i in gamut3)
    def _add_blocks_y(self,block1,block2):
        b1h=block1[0].count("\n")+1
        return block1[0]+"\n"+block2[0],block1[1]+tuple((i[0],i[1]+b1h) for i in block2[1])
    def _make_block(self,joint,joinr,joinb,joinl,room=True):
        max_width=16
        max_height=9
        xmiddle=8
        ymiddle=5
        max_iwidth=max_width-4
        max_iheight=max_height-4
        min_iwidth=2
        min_iheight=2
        if room:
            iwidth=random.randint(min_iwidth,max_iwidth)
            iheight=random.randint(min_iheight,max_iheight)
        else:
            iwidth=iheight=-2
        width=iwidth+2
        height=iheight+2
        max_xoffset=max_width-width-1
        max_yoffset=max_height-height-1
        xoffset=random.randint(1,max_xoffset)
        yoffset=random.randint(1,max_yoffset)
        if room:
            topdoor=random.randrange(iwidth)+xoffset+1
            botdoor=random.randrange(iwidth)+xoffset+1
            leftdoor=random.randrange(iheight)+yoffset+1
            rightdoor=random.randrange(iheight)+yoffset+1
            #
            block=""
            for j in range(max_height):
                if j<yoffset:
                    block+=" "*max_width+"\n"
                elif j==yoffset:
                    line=list(" "*xoffset+"g"+"o"*iwidth+"G"+" "*(max_width-(iwidth+xoffset+2)))
                    if joint:
                        line[topdoor]="."
                    block+="".join(line)+"\n"
                elif j<(yoffset+1+iheight):
                    line=list(" "*xoffset+"d"+"."*iwidth+"d"+" "*(max_width-(iwidth+xoffset+2)))
                    if joinl and j==leftdoor:
                        line[xoffset]="."
                    if joinr and j==rightdoor:
                        line[xoffset+iwidth+1]="."
                    block+="".join(line)+"\n"
                elif j==(yoffset+1+iheight):
                    line=list(" "*xoffset+"j"+"o"*iwidth+"J"+" "*(max_width-(iwidth+xoffset+2)))
                    if joinb:
                        line[botdoor]="."
                    block+="".join(line)+"\n"
                elif j>(yoffset+iheight):
                    block+=" "*max_width+"\n"
        else:
            topdoor=botdoor=xoffset
            leftdoor=rightdoor=yoffset
            block=(" "*max_width+"\n")*max_height
        block=block.strip("\n")
        #
        block=[list(i) for i in block.split("\n")]
        doors=[(joint,[xmiddle,0],[topdoor,yoffset-1]), (joinb,[xmiddle,max_height-1],[botdoor,yoffset+1+iheight+1]), (joinl,[0,ymiddle],[xoffset-1,leftdoor]), (joinr,[max_width-1,ymiddle],[xoffset+1+iwidth+1,rightdoor])]
        for conditional,to,from_ in doors:
            if conditional:
                while 1:
                    block[int(from_[1])][int(from_[0])]="."
                    if from_[0]==to[0] and from_[1]==to[1]:
                        break
                    vector_angle=math.atan2(abs(from_[1]-to[1]),abs(from_[0]-to[0]))
                    vector_angle*=180
                    vector_angle/=math.pi
                    vector_angle=int(vector_angle+0.5)
                    if vector_angle>45:
                        from_[1]-=(from_[1]-to[1])/abs(from_[1]-to[1])
                    else:
                        from_[0]-=(from_[0]-to[0])/abs(from_[0]-to[0])
        block="\n".join(["".join(i) for i in block])
        #
        self._ag=(xoffset+1,yoffset+1)
        gamut=[]
        gamutx=range(xoffset+1,xoffset+1+iwidth)
        gamuty=range(yoffset+1,yoffset+1+iheight)
        for x in gamutx:
            for y in gamuty:
                gamut.append((x,y))
        return block,tuple(gamut)
    def genmap(self):
        roomyes=[True,True,True,True,True,True]
        for i in range(random.randrange(3)+1):
            roomyes[random.randrange(6)]=False
        self.coded_grid,self.gamut=self._add_blocks_y(self._add_blocks_x(self._make_block(0,1,1,0,roomyes[0]),self._make_block(0,1,0,1,roomyes[1]),self._make_block(0,0,1,1,roomyes[2])),self._add_blocks_x(self._make_block(1,1,0,0,roomyes[3]),self._make_block(0,1,0,1,roomyes[4]),self._make_block(1,0,0,1,roomyes[5])))
        self.gamut=list(self.gamut)
        self.readmap()

