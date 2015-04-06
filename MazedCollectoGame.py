from repugeng.MazeLevel import MazeLevel
from repugeng.DumbFovLevel import DumbFovLevel
from BasicCollectoGame import BasicCollectoGame

class MazedCollectoGame(MazeLevel,BasicCollectoGame):
    nsiz=8 #Cannot be bigger than 8
    title_window="Repuge-NG Collecto: Maze Edition"
#
if __name__=="__main__":
    l=MazedCollectoGame()
