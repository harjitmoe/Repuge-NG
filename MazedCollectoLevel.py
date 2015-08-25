from prelevula.MazeLevel2 import MazeLevel2
from CollectoInterface import CollectoInterface
from CollectoLevel import CollectoLevel
from CollectoGame import CollectoGame

class MazedCollectoLevel(CollectoLevel,MazeLevel2):
    InterfaceClass=CollectoInterface
    title_window="Repuge-NG Collecto: Maze"
CollectoGame.register_leveltype(MazedCollectoLevel)
#
if __name__=="__main__":
    CollectoGame()
