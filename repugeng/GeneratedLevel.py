from repugeng.Level import Level

class GeneratedLevel(Level):
    """Base class for a generated (rather than predefined) level.
    
    Genral subclasses should override genmap().
    Levels may override initmap() and NOT readmap() or genmap().
    
    Notable attributes and methods, additional to that from Level:
    - initmap() - initialise map.  Should call genmap().
    - genmap() - regenerate the map.  May call readmap().
    - gamut - a list of coord-tuples safe to initially deposit 
      objects or players on.  Not necessarily the entire traversable
      area.
    """
    gamut=None
    nsiz=0
    def initmap(self):
        """Initialise map.

        May be overridden by level.  Should not be overridden by 
        general subclass.  Should call genmap()."""
        self.genmap()
    def genmap(self,*args,**kwargs):
        """Generate map.  (Creates self.grid and self.objgrid.)

        May call readmap().  Should be implemented by subclass.
        Should not be overridden by level.
        
        *args, **kwargs: anything of interest to general subclass."""
        raise NotImplementedError("should be implemented by subclass")
