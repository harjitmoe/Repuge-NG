from prelevula.MazeLevel import MazeLevel
from CollectoInterface import CollectoInterface
from CollectoGame import CollectoGame

class MazedCollectoGame(CollectoGame,MazeLevel):
    InterfaceClass=CollectoInterface
    title_window="Repuge-NG Collecto: Maze"
CollectoGame.register_leveltype(MazedCollectoGame)
#
if __name__=="__main__":
    MazedCollectoGame()
