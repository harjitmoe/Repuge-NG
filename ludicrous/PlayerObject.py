from ludicrous.GridObject import GridObject

__copying__="""
Written by Thomas Hori

This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/."""

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
