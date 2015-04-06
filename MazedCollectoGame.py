from repugenglevelgens.MazeLevel import MazeLevel
from repugeng.DumbFovLevel import DumbFovLevel
from CollectoGame import CollectoGame

class MazedCollectoGame(CollectoGame,DumbFovLevel,MazeLevel):
    title_window="Repuge-NG Collecto: Maze"
CollectoGame.register_leveltype(MazedCollectoGame)
#
if __name__=="__main__":
    MazedCollectoGame()
