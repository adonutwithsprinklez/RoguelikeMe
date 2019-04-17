


class Tile(object):
    def __init__(self, draw_icon = " ", view_passed=True, walkable=None):
        self.icon = draw_icon
        self.viewPassed = view_passed
        
        # Defaults to viewPassed, otherwise goes to whatever is passed
        if walkable:
            self.walkable = walkable
        else:
            self.walkable = self.viewPassed
    
    def getWalkable(self):
        return self.walkable
    
    def getViewable(self):
        return self.viewPassed


class MapObject(object):
    def __init__(self):
        pass