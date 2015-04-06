from repugenglevelgens.RoomLevel import RoomLevel
from repugeng.DumbFovLevel import DumbFovLevel
from CollectoGame import CollectoGame

class BasicCollectoGame(CollectoGame,DumbFovLevel,RoomLevel):
    title_window="Repuge-NG Collecto: Room"
CollectoGame.register_leveltype(BasicCollectoGame)
#
if __name__=="__main__":
    BasicCollectoGame()
