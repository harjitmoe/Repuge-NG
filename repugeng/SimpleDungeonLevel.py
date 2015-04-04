from repugeng.Level import Level
import random,math

class SimpleDungeonLevel(Level):
    """Level subclass for a simple rogue-like dungeon.

    Simple in that at will always contain exactly 6 rooms,
    connected in a ring."""
    list_of_symbols={"g":"wall_corner_nw","G":"wall_corner_ne","j":"wall_corner_sw","J":"wall_corner_se","d":"vwall","o":"hwall",":":"vfeature","*":"vfeature"," ":"space",".":"floor1",",":"floor2","/":"floor3","$":"floor4","#":"floor5","P":"hfeature","l":"hfeature","v":"wall_TeeJnc_dn","^":"wall_TeeJnc_up",">":"wall_TeeJnc_rt","<":"wall_TeeJnc_lt","+":"wall_cross",}
    def _add_blocks_x(self,block1,block2,block3):
        block4=[]
        for line1,line2,line3 in zip(block1.split("\n"),block2.split("\n"),block3.split("\n")):
            block4.append(line1+line2+line3)
        return "\n".join(block4)
    def _make_block(self,joint,joinr,joinb,joinl):
        max_width=16
        max_height=9
        xmiddle=8
        ymiddle=5
        max_iwidth=max_width-4
        max_iheight=max_height-4
        min_iwidth=2
        min_iheight=2
        iwidth=random.randint(min_iwidth,max_iwidth)
        iheight=random.randint(min_iheight,max_iheight)
        width=iwidth+2
        height=iheight+2
        max_xoffset=max_width-width-1
        max_yoffset=max_height-height-1
        xoffset=random.randint(1,max_xoffset)
        yoffset=random.randint(1,max_yoffset)
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
        block=block.strip("\n")
        #
        block=[list(i) for i in block.split("\n")]
        doors=[(joint,[xmiddle,0],[topdoor,yoffset-1]), (joinb,[xmiddle,max_height-1],[botdoor,yoffset+1+iheight+1]), (joinl,[0,ymiddle],[xoffset-1,leftdoor]), (joinr,[max_width-1,ymiddle],[xoffset+1+iwidth+1,rightdoor])]
        for conditional,to,from_ in doors:
            if conditional:
                while 1:
                    block[from_[1]][from_[0]]="."
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
        return block
    def readmap(self):
        b1=self._make_block(0,1,1,0)
        ag=self._ag
        self.coded_grid=self._add_blocks_x(b1,self._make_block(0,1,0,1),self._make_block(0,0,1,1))+"\n"+self._add_blocks_x(self._make_block(1,1,0,0),self._make_block(0,1,0,1),self._make_block(1,0,0,1))
        Level.readmap(self)
        self.starting_pt=ag

