# Repuge-NG: an engine for Roguelike games #

Written in Python.

Three components:
- Consolation: an interface for interfacing with terminals on multiple platforms (using WConio on Windows).  Could interface with a tiled display, but no such display code has been written (yet).  Supports serving displays remotely using XML-RPC.  API comparably stable.
- Ludicrous: a Roguelike game engine running on Consolation.  Supports multiple players (via remote Consolation displays).  API may still be subject to drastic changes.
- Prelevula: a few level generators for Ludicrous.
