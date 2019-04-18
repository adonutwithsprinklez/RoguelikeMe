
import random
import tcod as libtcod

from DrawOrderClass import BasicDrawOrder

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


class RegionObject(object):
    def __init__(self, region_data, width=40, height=40):
        self.data = region_data
        self.name = self.data["Name"]
        self.regionID = self.data["RegionID"]

        # Region dimensions
        self.width = width
        self.height = height
        self.chunk = []

        # Load tiles
        self.tiles = {}
        for tiledata in self.data["Tiles"]:
            tileID = tiledata["tileid"]
            tileIcon = tiledata["icon"]
            tileWalkable = tiledata["walkable"]
            tilePassable = tiledata["viewable"]
            tileColor = tiledata["color"]
            self.tiles[tileID] = Tile(tileIcon, tilePassable, tileWalkable, tileColor)
        
        # Load generation instructions
        self.generationInstructions = []
        for instruction in self.data["Generation"]:
            instructID = instruction[0]
            if len(instruction) > 1:
                instructArgs = instruction[1:]
                newstep = (instructID, instructArgs)
            else:
                newstep = (instructID)
            self.generationInstructions.append(newstep)
    
    def generateWorld(self):
        self.chunk = []
        for x in range(0, self.width):
            column = []
            for y in range(0, self.height):
                column.append(None)
            self.chunk.append(column)
        
        for instruction in self.generationInstructions:
            command = instruction[0]
            args = instruction[1]

            if command == "fill_rect":
                self.fillRect(args)
            elif command == "place_random":
                self.placeRandom(args)
    
    # Generation functions
    def fillRect(self, args):
        filltiles = args[0]
        startx = args[1]
        starty = args[2]
        endx = args[3]
        endy = args[4]
        if startx == -1:
            startx = self.width-1
        if starty == -1:
            starty = self.height-1
        if endx == -1:
            endx = self.width
        if endy == -1:
            endy = self.height
        x = startx
        for column in self.chunk[startx:endx]:
            y = starty
            for tile in column[starty:endy]:
                self.chunk[x][y] = random.choice(filltiles)
                y+=1
            x+=1
        self.chunk[0][0] = "wall"
        self.chunk[39][39] = "wall"
    
    def placeRandom(self,args):
        filltiles = args[0]
        startx = args[1]
        starty = args[2]
        endx = args[3]
        endy = args[4]
        numToPlace = args[5]
        if startx == -1:
            startx = self.width-1
        if starty == -1:
            starty = self.height-1
        if endx == -1:
            endx = self.width-1
        if endy == -1:
            endy = self.height-1
        for i in range(0,numToPlace):
            x,y = random.randint(startx,endx), random.randint(starty,endy)
            self.chunk[x][y] = random.choice(filltiles)
        
    # Getter functions
    def getDrawOrders(self, map_console):
        drawOrders = []
        x = 0
        for column in self.chunk:
            y = 0
            for tile in column:
                if tile:
                    tileicon = self.tiles[tile].icon
                    tilecolor = self.tiles[tile].color
                else:
                    tileicon = " "
                    tilecolor = None
                newOrder = BasicDrawOrder(map_console,tileicon,tilecolor,x,y)
                drawOrders.append(newOrder)
                y+=1
            x+=1
        return drawOrders
    
    def getWalkable(self, x=0, y=0):
        walkable = self.tiles[self.chunk[x][y]].getWalkable()
        return walkable


class MapObject(object):
    def __init__(self):
        pass