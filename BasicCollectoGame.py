from prelevula.RoomLevel import RoomLevel
from repugeng.DumbFovInterface import DumbFovInterface
from CollectoGame import CollectoGame

class BasicCollectoGame(CollectoGame,RoomLevel):
    InterfaceClass=DumbFovInterface
    title_window="Repuge-NG Collecto: Room"
CollectoGame.register_leveltype(BasicCollectoGame)
#
if __name__=="__main__":
    BasicCollectoGame()
