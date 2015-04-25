from repugeng.SimpleInterface import SimpleInterface

class ScrollingInterface(SimpleInterface):
    def get_viewport_grids(self):
        width=79
        height=19
        offsetx=self.playerobj.pt[0]-(width//2)
        offsety=self.playerobj.pt[1]-(height//2)
        levwidth=len(self.level.grid)
        levheight=len(self.level.grid[0])
        colno=offsetx
        coords=[]
        grid_subset=[]
        objgrid_subset=[]
        for unused in range(width):
            if (colno>=0) and (colno<levwidth):
                gcol=self.level.grid[colno]
                ocol=self.level.objgrid[colno]
            c_sub=[]
            g_sub=[]
            o_sub=[]
            rowno=offsety
            for unused2 in range(height):
                c_sub.append((colno,rowno))
                if (colno<0) or (colno>=levwidth) or (rowno<0) or (rowno>=levheight):
                    g_sub.append(("space",None))
                    o_sub.append([])
                else:
                    g_sub.append(gcol[rowno])
                    o_sub.append(ocol[rowno])
                rowno+=1
            coords.append(c_sub)
            grid_subset.append(g_sub)
            objgrid_subset.append(o_sub)
            colno+=1
        return coords,grid_subset,objgrid_subset
    def get_viewport_pt(self):
        return 79//2,19//2
