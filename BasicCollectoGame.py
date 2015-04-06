from repugeng.RoomLevel import RoomLevel
from repugeng.DumbFovLevel import DumbFovLevel
from CollectoGameEngine import CollectoGameEngine

class BasicCollectoGame(CollectoGameEngine,DumbFovLevel,RoomLevel):
    title_window="Repuge-NG Collecto: Room"
CollectoGameEngine.register_leveltype(BasicCollectoGame)
#
if __name__=="__main__":
    BasicCollectoGame()
