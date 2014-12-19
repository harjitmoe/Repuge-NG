class ConsoleTiles(object):
    @classmethod
    def __new__(cls,*a,**kw):
        raise TypeError,"attempt to create instance of static class"
    space=" "
    vwall="|"
    hwall="-"
    wall_corner_nw="-" #In true Rogue style
    wall_corner_ne="-" #In true Rogue style
    wall_corner_sw="-" #In true Rogue style
    wall_corner_se="-" #In true Rogue style
    wall_TeeJnc_up="-" #In true continuation of Rogue style
    wall_TeeJnc_dn="-" #In true continuation of Rogue style
    wall_TeeJnc_rt="|" #In true continuation of Rogue style
    wall_TeeJnc_lt="|" #In true continuation of Rogue style
    wall_cross="-" #In true continuation of Rogue style
    vfeature=":"
    hfeature="="
    #Levels of floor
    floor1="."
    floor2=","
    floor3="/"
    floor4="$"
    floor5="#"
    user="@"
    fred="@"
    ron="@"
    hermione="@"
    quirrel="@"
    peeves="P"
    malfoy="M"
    crabbe="@"
    goyle="@"
    quirrel="@"
    gnome="G"
    flitwick="@"
    snail="S"
    tent="T"
    tentacle="~"
    sprout="@"
    sprout="\x02"
    bush="B"
    needle="~"
    chest="]"
    cauldron=")"
    doxy="D"
    snare="s"
    boulder="O"
    snape="@"
    ingredient="%"
    filtch="@"
    norris="&"
    fluffyhead="+"
    erised="}"
    dumbledore="@"
    bean="'"
    card='"'
    frog="f"
    extra="@"
    drink="!"
