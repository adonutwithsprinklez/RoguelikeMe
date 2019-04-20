
import tcod as libtcod

class Tile(object):
    def __init__(self, draw_icon = " ", view_passed=True, walkable=None, color=[255,255,255]):
        self.icon = draw_icon
        self.viewPassed = view_passed
        self.color = libtcod.Color(color[0], color[1], color[2])
        
        # Defaults to viewPassed, otherwise goes to whatever is passed
        if walkable:
            self.walkable = walkable
        else:
            self.walkable = self.viewPassed
    
    def getWalkable(self):
        return self.walkable
    
    def getViewable(self):
        return self.viewPassed