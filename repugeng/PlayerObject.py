from repugeng.GridObject import GridObject
class PlayerObject(GridObject):
    """ The default player object.
    """
    tile = "user"
    name = "player"
    appearance = "player"
    corpse_type = None
    vitality = 10 #Hit-points, enchantment level... depending on object
    maxhp = 10
    init_hp_interval = 5
