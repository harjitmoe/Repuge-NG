"""
Repuge-NG: Real educational/entertainment programs use game engines - Next Generation.

The original aim was to produce a framework in which an educational game could be 
written in Python, as a response to an extracurricular challenge at School.  That 
proved fairly abortive, but I kept the codebase.

My proposal for my entry contained the following summary of the original generation (REPUGE):

    On first hearing of this task, I had been playing NetHack (a dungeon-crawling game with a terminal interface) in both GUI and terminal interfaces, and it occurred to me that the GUI is the hardest part of the design (for me, anyway) and would be simpler if I created a simple Python-based framework to do the GUI in (for then) a Windows console. 
    
    The design considerations I used were thus: there should be three parts to any game: the level(s), the framework and the backend wrapper.  Because running the levels *under* the framework would make the framework significantly harder to produce and limit the capabilities of the level, I designed it so the framework plays only a supporting role in processing the level map (designed in a simple text-based format with symbols defined in the level as certain object types and kept around as an object attribute), invoking the level script and providing the internal map model and auxiliary subroutines/functions; the level script itself does the event looping and game logic.  The actual output is not done by the framework or the level but by a separate backend wrapper which deals with the actual appearance which could use any symbol for any object and output to a text terminal, flat birds eye display, isometric display or even direct3d as far as the rest of the game is concerned; this is to ease porting between textual/graphical interfaces and between OSs. 
    
    I called it REPUGE, for Real Educational Programs Use Game Engines.

For that project, see BasicCollectoGame.py amongst the example material.

This project, Repuge-NG, was an aim to refactor the loosely functional REPUGE code, where the meanings of x and y were not consistent across the API, into a tightly object-oriented framework which allows programs to be written which are actually readable.  Given that the event loop code seemed to be more-or-less the same across everything, I integrated it into the framework (it can be overridden by the level, though).

One version of REPUGE only displayed the area which is actually visible to the player, unless asked otherwise by the level.  The code for this was illegible, and the x-y confusion didn't help.  I scrapped it.  I may rewrite it at some point.
"""