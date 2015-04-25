from prelevula.RoomLevel import RoomLevel
from CollectoInterface import CollectoInterface
from CollectoGame import CollectoGame

class BasicCollectoGame(CollectoGame,RoomLevel):
    InterfaceClass=CollectoInterface
    title_window="Repuge-NG Collecto: Room"
CollectoGame.register_leveltype(BasicCollectoGame)
#
if __name__=="__main__":
    BasicCollectoGame()
