from repugeng.MazeLevel import MazeLevel
from repugeng.DumbFovLevel import DumbFovLevel
from CollectoGameEngine import CollectoGameEngine

class MazedCollectoGame(CollectoGameEngine,DumbFovLevel,MazeLevel):
    title_window="Repuge-NG Collecto: Maze"
CollectoGameEngine.register_leveltype(MazedCollectoGame)
#
if __name__=="__main__":
    MazedCollectoGame()
