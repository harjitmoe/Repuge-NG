from prelevula.SimpleDungeonLevel import SimpleDungeonLevel
from repugeng.DumbFovLevel import DumbFovLevel
from CollectoGame import CollectoGame

class DungeonCollectoGame(CollectoGame,DumbFovLevel,SimpleDungeonLevel):
    title_window="Repuge-NG Collecto: Dungeon"
CollectoGame.register_leveltype(DungeonCollectoGame)
#
if __name__=="__main__":
    DungeonCollectoGame()
