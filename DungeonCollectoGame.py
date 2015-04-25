from prelevula.SimpleDungeonLevel import SimpleDungeonLevel
from CollectoInterface import CollectoInterface
from CollectoGame import CollectoGame

class DungeonCollectoGame(CollectoGame,SimpleDungeonLevel):
    InterfaceClass=CollectoInterface
    title_window="Repuge-NG Collecto: Dungeon"
CollectoGame.register_leveltype(DungeonCollectoGame)
#
if __name__=="__main__":
    DungeonCollectoGame()
