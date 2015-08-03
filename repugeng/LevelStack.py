class LevelStack(object):
    """Simple level stack.  Does not accommodate branched levels."""
    def __init__(self,n,*objects):
        self.n=n
        self.stack=objects