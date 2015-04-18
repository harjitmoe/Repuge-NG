from prelevula.MazeLevel import MazeLevel
from repugeng.DumbFovInterface import DumbFovInterface
from CollectoGame import CollectoGame

class MazedCollectoGame(CollectoGame,MazeLevel):
    InterfaceClass=DumbFovInterface
    title_window="Repuge-NG Collecto: Maze"
CollectoGame.register_leveltype(MazedCollectoGame)
#
if __name__=="__main__":
    MazedCollectoGame()
