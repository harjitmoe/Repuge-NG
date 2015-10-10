from prelevula.SimpleDungeonLevel import SimpleDungeonLevel
from CollectoInterface import CollectoInterface
from CollectoLevel import CollectoLevel
from CollectoGame import CollectoGame

class DungeonCollectoLevel(CollectoLevel, SimpleDungeonLevel):
    InterfaceClass = CollectoInterface
    title_window = "Ludicrous Collecto: Dungeon"
CollectoGame.register_leveltype(DungeonCollectoLevel)
#
if __name__ == "__main__":
    CollectoGame()
