from repugeng.SimpleDungeonLevel import SimpleDungeonLevel
from repugeng.DumbFovLevel import DumbFovLevel
from CollectoGameEngine import CollectoGameEngine

class DungeonCollectoGame(CollectoGameEngine,DumbFovLevel,SimpleDungeonLevel):
    title_window="Repuge-NG Collecto: Dungeon"
CollectoGameEngine.register_leveltype(DungeonCollectoGame)
#
if __name__=="__main__":
    DungeonCollectoGame()
