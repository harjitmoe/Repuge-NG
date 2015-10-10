from prelevula.RoomLevel import RoomLevel
from CollectoInterface import CollectoInterface
from CollectoLevel import CollectoLevel
from CollectoGame import CollectoGame

class BasicCollectoLevel(CollectoLevel, RoomLevel):
    InterfaceClass = CollectoInterface
    title_window = "Ludicrous Collecto: Room"
CollectoGame.register_leveltype(BasicCollectoLevel)
#
if __name__ == "__main__":
    CollectoGame()
